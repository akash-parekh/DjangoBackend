from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Employee, Document, Assignment
from .forms import DocForm

# Create your views here.

@api_view(['GET'])
def BoardData(request):
    docQ = Document.objects.values().all()
    assignQ = Assignment.objects.values().all()
    print(docQ)
    print(assignQ)
    
    assignData = []
    underProcessData = []
    processedData = []
    underReviewData = []
    reviewedData = []
    
    for i in range (len(docQ)):
        if(docQ[i]['status'] == 'Assigned'):
            assignData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'],
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['process_emp_id'],
                "logs":[f"Document created at {docQ[i]['date_added']} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}"],
                "status": 'Assigned'
            })
        elif(docQ[i]['status'] == 'UnderProcess'):
            underProcessData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'],
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['process_emp_id'],
                "logs":[f"Document created at {docQ[i]['date_added']} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}"],
                "status": 'Under Process'
            })
        elif(docQ[i]['status'] == 'Processed'):
            processedData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'],
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['review_emp_id'],
                "logs":[f"Document created at {docQ[i]['date_added']} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}", f"Document Processed at {docQ[i]['date_processed']} ({docQ[i]['time_to_process']})", f"Document Assigned to {assignQ[i]['review_emp_id']}"],
                "status": 'Processed'
            })
        elif(docQ[i]['status'] == 'UnderReview'):
            underReviewData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'],
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['review_emp_id'],
                "logs":[f"Document created at {docQ[i]['date_added']} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}", f"Document Processed at {docQ[i]['date_processed']} ({docQ[i]['time_to_process']})", f"Document Assigned to {assignQ[i]['review_emp_id']}"],
                "status": 'Under Review'
            })
        elif(docQ[i]['status'] == 'Reviewed'):
            reviewedData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'],
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['review_emp_id'],
                "logs":[f"Document created at {docQ[i]['date_added']} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}", f"Document Processed at {docQ[i]['date_processed']} ({docQ[i]['time_to_process']})", f"Document Assigned to {assignQ[i]['review_emp_id']}", f"Document Completed at {docQ[i]['date_reviwed']} ({docQ[i]['time_to_review']})", f"Total Time Take to Complete the document - {docQ[i]['total_time']}"],
                "status": 'Completed'
            })
        
    columns = [{
            "name": "Assigned",
            "tasks": assignData, 
        },{
            "name": "Under Process",
            "tasks": underProcessData, 
        },{
            "name": "Processed",
            "tasks": processedData,
        },{
            "name": "Under Review",
            "tasks": underReviewData,
        },{
            "name": "Completed",
            "tasks": reviewedData
        }]
    
    return Response(columns)

@api_view(['GET','POST'])
def DocUpdate(request, id):
    docQ = Document.objects.values().get(pk = id)
    assignQ = Assignment.objects.get(doc_id_id = id) 
    print("Here")
    print("",docQ, assignQ)
    if request.method == 'POST':
        assignQ.status = request.data['status']
        assignQ.save(update_fields=['status'])
        updatedDoc = Document.objects.values().get(pk = id)
        return Response({"Message": "Updated", "data": updatedDoc})
    
    elif request.method == 'GET':
        return Response(docQ)
                