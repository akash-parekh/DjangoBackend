from django.db import models
from django.db.models import Count
from django.utils.timezone import now

import pandas as pd

# Create your models here.

class Employee(models.Model):
    emp_name = models.CharField(max_length=100)
    emp_id = models.CharField(max_length=50, primary_key=True)
    
    def __str__(self):
        return f"{self.emp_id}"
    
class Document(models.Model):
    class Operation(models.TextChoices):
        NEW = 'New'
        ASSIGNED = 'Assigned'
        UNDER_PROCESS = 'Under Process'
        PROCESSED = 'Processed'
        UNDER_REVIEW = 'Under Review'
        REVIEWED = 'Reviewed'
    
    class Complexity(models.TextChoices):
        SIMPLE = 'Simple'
        COMPLEX = 'Complex'
        VERY_COMPLEX = 'Very Complex'
        
    class Type(models.TextChoices):
        BLSHEET = 'Balance Sheet'
        INCSTMNT = 'Income Statement'
        CFSSTMNT = 'Cash Flow Statement'
        
    doc_name = models.CharField(max_length=100)
    doc_id = models.CharField(max_length=50, primary_key=True)
    status = models.CharField(max_length=20, choices=Operation.choices, default=Operation.NEW, editable=False)
    complexity =  models.CharField(max_length=20, choices=Complexity.choices, default=Complexity.SIMPLE)
    type = models.CharField(max_length=30, choices=Type.choices, default=Type.BLSHEET)   
    date_added = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True, blank=True, editable=False)
    date_reviwed = models.DateTimeField(null=True, blank=True, editable=False)
    total_time = models.CharField(max_length=15, blank=True, editable=False)
    time_to_process = models.CharField(max_length=10, blank=True, editable=False)
    time_to_review = models.CharField(max_length=10, blank=True, editable=False)
    NoOfRechecks = models.IntegerField(blank=True, default=0)
    documentTrail = models.TextField(blank=True, default="")
    
    def __str__(self):
        return f"{self.doc_id}"
    
    def save(self, *args, **kwargs):
        if self.status == self.Operation.NEW:
            self.documentTrail += f"Document created at {self.date_added.strftime('%m/%d/%Y, %H:%M:%S')} of type {self.type} and complexity {self.complexity}.\r\n"
            super().save(*args, **kwargs)
            newQ = Document.objects.all().order_by('-date_added')
            empQ = Employee.objects.all()
            assignProcessQ = Assignment.objects.values('process_emp').annotate(Count('process_emp')).order_by('process_emp__count')
            assignReviewQ = Assignment.objects.values('review_emp').annotate(Count('review_emp')).order_by('review_emp__count')
            print("HERE   ", assignProcessQ, assignReviewQ)
            emp1 =  assignProcessQ[0]['process_emp'] if assignProcessQ else empQ[0]
            emp2 = assignReviewQ[0]['review_emp'] if assignReviewQ else empQ[1]
            if emp1 == emp2:
                emp2 = assignReviewQ[1]['review_emp']
            process_emp = Employee.objects.get(emp_id = emp1)
            review_emp = Employee.objects.get(emp_id = emp2)
            createNew = Assignment(doc_id = newQ[0], process_emp = process_emp, review_emp = review_emp, status = self.Operation.ASSIGNED)
            createNew.save()
            return
        elif self.status == self.Operation.ASSIGNED:
            assignQ = Assignment.objects.get(doc_id=self.doc_id)
            self.documentTrail += f"Document Assigned to {assignQ.process_emp_id}.\r\n"
        elif self.status == self.Operation.UNDER_PROCESS:
            self.date_processed = now()
        elif self.status == self.Operation.PROCESSED:
            assignQ = Assignment.objects.get(doc_id=self.doc_id)
            self.time_to_process = (now() - self.date_processed)
            self.date_processed = now()
            self.documentTrail += f"Document Processed at {self.date_processed.strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(self.time_to_process).total_seconds() / 60)} minutes). \r\nDocument Assigned to {assignQ.review_emp_id}. \r\n"
        elif self.status == self.Operation.UNDER_REVIEW:
            self.NoOfRechecks += 1
            self.date_reviwed = now()
        elif self.status == self.Operation.REVIEWED:
            self.time_to_review = (now() - self.date_reviwed)
            self.date_reviwed = now()
            self.total_time = now() - self.date_added
            self.documentTrail += f"Document Completed at {self.date_reviwed.strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(self.time_to_review).total_seconds() / 60)} minutes). \r\nTotal Time Take to Complete the document - {int(pd.Timedelta(self.total_time).total_seconds() / 60)} minutes. \r\n"
        return super().save(*args, **kwargs)
            
    
class Assignment(models.Model):
    class Operation(models.TextChoices):
        NEW = 'New'
        ASSIGNED = 'Assigned'
        UNDER_PROCESS = 'Under Process'
        PROCESSED = 'Processed'
        UNDER_REVIEW = 'Under Review'
        REVIEWED = 'Reviewed'
    doc_id = models.ForeignKey(Document, on_delete=models.CASCADE, unique=True)
    process_emp = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='ProcessedByEmp')
    review_emp = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='ReviewedByEmp')
    status = models.CharField(max_length=20, choices=Operation.choices)
    
    def __str__(self):
        return f"{self.doc_id} - Emp Process: {self.process_emp} - Emp Review: {self.review_emp} - {self.status}"
    
    def save(self, *args, **kwargs):
        try:
            doc = Document.objects.get(pk = self.doc_id)
            doc.status = self.status
            doc.save()
        except Document.DoesNotExist:
            print('Document does not exist')
        return super().save(*args, **kwargs)