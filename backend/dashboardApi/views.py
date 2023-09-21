from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
import pandas as pd
from datetime import datetime

from .models import Employee, Document, Assignment
from .forms import DocForm

# Create your views here.

@api_view(['GET'])
def BoardData(request):
    docQ = Document.objects.values().all()
    assignQ = Assignment.objects.values().all()
    
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
                "date_added": docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['process_emp_id'],
                # "logs":[f"Document created at {docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}"],
                "status": 'Assigned',
                "documentTrail": docQ[i]['documentTrail'].split('\r\n')
            })
        elif(docQ[i]['status'] == 'Under Process'):
            underProcessData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['process_emp_id'],
                # "logs":[f"Document created at {docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}"],
                "status": 'Under Process',
                "documentTrail": docQ[i]['documentTrail'].split('\r\n')
            })
        elif(docQ[i]['status'] == 'Processed'):
            processedData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['review_emp_id'],
                # "logs":[f"Document created at {docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}", f"Document Processed at {docQ[i]['date_processed'].strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(docQ[i]['time_to_process']).total_seconds() / 60)} minutes)", f"Document Assigned to {assignQ[i]['review_emp_id']}"],
                "status": 'Processed',
                "documentTrail": docQ[i]['documentTrail'].split('\r\n')
            })
        elif(docQ[i]['status'] == 'Under Review'):
            underReviewData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['review_emp_id'],
                # "logs":[f"Document created at {docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}", f"Document Processed at {docQ[i]['date_processed'].strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(docQ[i]['time_to_process']).total_seconds() / 60)} minutes)", f"Document Assigned to {assignQ[i]['review_emp_id']}"],
                "status": 'Under Review',
                "documentTrail": docQ[i]['documentTrail'].split('\r\n')
                # "documentTrail": docQ[i]['documentTrail'].split('\r\n').split(),
                # "recheck": docQ[i]['reCheck']
            })
        elif(docQ[i]['status'] == 'Reviewed'):
            reviewedData.append({
                "title": docQ[i]['doc_name'],
                "Id": docQ[i]['doc_id'],
                "date_added": docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": docQ[i]['type'],
                "complexity": docQ[i]['complexity'],
                "empId": assignQ[i]['review_emp_id'],
                # "logs":[f"Document created at {docQ[i]['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {docQ[i]['type']} and complexity {docQ[i]['complexity']}", f"Document Assigned to {assignQ[i]['process_emp_id']}", f"Document Processed at {docQ[i]['date_processed'].strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(docQ[i]['time_to_process']).total_seconds() / 60)} minutes)", f"Document Assigned to {assignQ[i]['review_emp_id']}", f"Document Completed at {docQ[i]['date_reviwed'].strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(docQ[i]['time_to_review']).total_seconds() / 60)} minutes)", f"Total Time Take to Complete the document - {int(pd.Timedelta(docQ[i]['total_time']).total_seconds() / 60)} minutes"],
                "status": 'Completed',
                "documentTrail": docQ[i]['documentTrail'].split('\r\n')
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
    if request.method == 'POST':
        assignQ.status = request.data['status']
        assignQ.save(update_fields=['status'])
        # if request.data['type']:
        #     docQ.type = request.data['type']
        #     docQ.save(update_fields=['type'])
        # if request.data['complexity']:
        #     docQ.complexity = request.data['complexity']
        #     docQ.save(update_fields=['complexity'])
        updatedDoc = Document.objects.values().get(pk = id)
        LatestAssign = Assignment.objects.values().get(doc_id_id = id)
        if(updatedDoc['status'] == 'Assigned'):
            payload = {
                "title": updatedDoc['doc_name'],
                "Id": updatedDoc['doc_id'],
                "date_added": updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": updatedDoc['type'],
                "complexity": updatedDoc['complexity'],
                "empId": LatestAssign['process_emp_id'],
                # "logs":[f"Document created at {updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {updatedDoc['type']} and complexity {updatedDoc['complexity']}", f"Document Assigned to {LatestAssign['process_emp_id']}"],
                "status": 'Assigned',
                "documentTrail": updatedDoc['documentTrail'].split('\r\n')
            }
        elif(updatedDoc['status'] == 'Under Process'):
            payload = {
                "title": updatedDoc['doc_name'],
                "Id": updatedDoc['doc_id'],
                "date_added": updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": updatedDoc['type'],
                "complexity": updatedDoc['complexity'],
                "empId": LatestAssign['process_emp_id'],
                # "logs":[f"Document created at {updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {updatedDoc['type']} and complexity {updatedDoc['complexity']}", f"Document Assigned to {LatestAssign['process_emp_id']}"],
                "status": 'Under Process',
                "documentTrail": updatedDoc['documentTrail'].split('\r\n')
            }
        elif(updatedDoc['status'] == 'Processed'):
            payload = {
                "title": updatedDoc['doc_name'],
                "Id": updatedDoc['doc_id'],
                "date_added": updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": updatedDoc['type'],
                "complexity": updatedDoc['complexity'],
                "empId": LatestAssign['review_emp_id'],
                # "logs":[f"Document created at {updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {updatedDoc['type']} and complexity {updatedDoc['complexity']}", f"Document Assigned to {LatestAssign['process_emp_id']}", f"Document Processed at {updatedDoc['date_processed'].strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(updatedDoc['time_to_process']).total_seconds() / 60)} minutes)", f"Document Assigned to {LatestAssign['review_emp_id']}"],
                "status": 'Processed',
                "documentTrail": updatedDoc['documentTrail'].split('\r\n')
            }
        elif(updatedDoc['status'] == 'Under Review'):
            payload = {
                "title": updatedDoc['doc_name'],
                "Id": updatedDoc['doc_id'],
                "date_added": updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": updatedDoc['type'],
                "complexity": updatedDoc['complexity'],
                "empId": LatestAssign['review_emp_id'],
                # "logs":[f"Document created at {updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {updatedDoc['type']} and complexity {updatedDoc['complexity']}", f"Document Assigned to {LatestAssign['process_emp_id']}", f"Document Processed at {updatedDoc['date_processed'].strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(updatedDoc['time_to_process']).total_seconds() / 60)} minutes)", f"Document Assigned to {LatestAssign['review_emp_id']}"],
                "status": 'Under Review',
                "documentTrail": updatedDoc['documentTrail'].split('\r\n')
            }
        elif(updatedDoc['status'] == 'Reviewed'):
            payload = {
                "title": updatedDoc['doc_name'],
                "Id": updatedDoc['doc_id'],
                "date_added": updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": updatedDoc['type'],
                "complexity": updatedDoc['complexity'],
                "empId": LatestAssign['review_emp_id'],
                # "logs":[f"Document created at {updatedDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {updatedDoc['type']} and complexity {updatedDoc['complexity']}", f"Document Assigned to {LatestAssign['process_emp_id']}", f"Document Processed at {updatedDoc['date_processed'].strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(updatedDoc['time_to_process']).total_seconds() / 60)} minutes)", f"Document Assigned to {LatestAssign['review_emp_id']}", f"Document Completed at {updatedDoc['date_reviwed'].strftime('%m/%d/%Y, %H:%M:%S')} ({int(pd.Timedelta(updatedDoc['time_to_review']).total_seconds() / 60)} minutes)", f"Total Time Take to Complete the document - {int(pd.Timedelta(updatedDoc['total_time']).total_seconds() / 60)} minutes"],
                "status": 'Completed',
                "documentTrail": updatedDoc['documentTrail'].split('\r\n')
            }
        return Response({"Message": "Updated", "data": payload})
    
    elif request.method == 'GET':
        return Response(docQ)
    
@api_view(['GET','POST'])
def Docs(request):
    docQ = Document.objects.values().all()
    if request.method == 'GET':
        return Response(docQ)
    elif request.method == 'POST':
        NewQuery = Document(doc_name = request.data['doc_name'], doc_id = request.data['doc_id'], type = request.data['type'], complexity = request.data['complexity'])
        NewQuery.save()
        LatestDoc = Document.objects.values().get(pk = request.data['doc_id'])
        LatestAssign = Assignment.objects.values().get(doc_id_id = request.data['doc_id'])
        payload = {
                "title": LatestDoc['doc_name'],
                "Id": LatestDoc['doc_id'],
                "date_added": LatestDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S'),
                "type": LatestDoc['type'],
                "complexity": LatestDoc['complexity'],
                "empId": LatestAssign['review_emp_id'],
                # "logs":[f"Document created at {LatestDoc['date_added'].strftime('%m/%d/%Y, %H:%M:%S')} of type {LatestDoc['type']} and complexity {LatestDoc['complexity']}"], 
                "status": 'Assigned',
                "documentTrail": LatestDoc['documentTrail'].split('\r\n')
            }
        return Response({"Message": "New Document Created", "data": payload})
                
                
                
@api_view(['GET'])
def Dashboard(request):
    simpleDoc = Document.objects.values('doc_id').filter(complexity='Simple')
    simpleAssign = Assignment.objects.values('process_emp_id').annotate(num_docs = Count('doc_id')).filter(doc_id__in = simpleDoc)
    complexDoc = Document.objects.values('doc_id').filter(complexity='Complex')
    complexAssign = Assignment.objects.values('process_emp_id').annotate(num_docs = Count('doc_id')).filter(doc_id__in = complexDoc)
    veryComplexDoc = Document.objects.values('doc_id').filter(complexity='Very Complex')
    veryComplexAssign = Assignment.objects.values('process_emp_id').annotate(num_docs = Count('doc_id')).filter(doc_id__in = veryComplexDoc)
    simple = [0,0,0]
    complex = [0,0,0]
    veryComplex = [0,0,0]
    for i in range(0, simpleAssign.count()):
        if simpleAssign[i]['process_emp_id'] == 'EmpOne':
            simple[0] = simpleAssign[i]['num_docs']
        elif simpleAssign[i]['process_emp_id'] == 'EmpTwo':
            simple[1] = simpleAssign[i]['num_docs']
        else:
            simple[2] = simpleAssign[i]['num_docs']
    
    for i in range(0, complexAssign.count()):
        if complexAssign[i]['process_emp_id'] == 'EmpOne':
            complex[0] = complexAssign[i]['num_docs']
        elif complexAssign[i]['process_emp_id'] == 'EmpTwo':
            complex[1] = complexAssign[i]['num_docs']
        else:
            complex[2] = complexAssign[i]['num_docs']
            
    for i in range(0, veryComplexAssign.count()):
        if veryComplexAssign[i]['process_emp_id'] == 'EmpOne':
            veryComplex[0] = veryComplexAssign[i]['num_docs']
        elif veryComplexAssign[i]['process_emp_id'] == 'EmpTwo':
            veryComplex[1] = veryComplexAssign[i]['num_docs']
        else:
            veryComplex[2] = veryComplexAssign[i]['num_docs']
    chart1 =[
            ['Employee ID', 'Simple', 'Complex', 'Very Complex'],
            ['EmpOne', simple[0], complex[0], veryComplex[0]],
            ['EmpTwo', simple[1], complex[1], veryComplex[1]],
            ['EmpThree', simple[2], complex[2], veryComplex[2]],
        ]
    
    
    BLDoc = Document.objects.values('doc_id').filter(type='Balance Sheet')
    BLAssign = Assignment.objects.values('process_emp_id').annotate(num_docs = Count('doc_id')).filter(doc_id__in = BLDoc)
    CFSDoc = Document.objects.values('doc_id').filter(type='Cash Flow Statement')
    CFSAssign = Assignment.objects.values('process_emp_id').annotate(num_docs = Count('doc_id')).filter(doc_id__in = CFSDoc)
    ISDoc = Document.objects.values('doc_id').filter(type='Income Statement')
    ISAssign = Assignment.objects.values('process_emp_id').annotate(num_docs = Count('doc_id')).filter(doc_id__in = ISDoc)
    BL = [0,0,0]
    CFS = [0,0,0]
    IS = [0,0,0]
    for i in range(0, BLAssign.count()):
        if BLAssign[i]['process_emp_id'] == 'EmpOne':
            BL[0] = BLAssign[i]['num_docs']
        elif BLAssign[i]['process_emp_id'] == 'EmpTwo':
            BL[1] = BLAssign[i]['num_docs']
        else:
            BL[2] = BLAssign[i]['num_docs']
    
    for i in range(0, CFSAssign.count()):
        if CFSAssign[i]['process_emp_id'] == 'EmpOne':
            CFS[0] = CFSAssign[i]['num_docs']
        elif CFSAssign[i]['process_emp_id'] == 'EmpTwo':
            CFS[1] = CFSAssign[i]['num_docs']
        else:
            CFS[2] = CFSAssign[i]['num_docs']
            
    for i in range(0, ISAssign.count()):
        if ISAssign[i]['process_emp_id'] == 'EmpOne':
            IS[0] = ISAssign[i]['num_docs']
        elif ISAssign[i]['process_emp_id'] == 'EmpTwo':
            IS[1] = ISAssign[i]['num_docs']
        else:
            IS[2] = ISAssign[i]['num_docs']

    chart2 =[
            ['Employee ID', 'Balance Sheet', 'Cash Flow Statement', 'Income Statement'],
            ['EmpOne', BL[0], CFS[0], IS[0]],
            ['EmpTwo', BL[1], CFS[1], IS[1]],
            ['EmpThree', BL[2], CFS[2], IS[2]],
        ]
    
    statusDoc = Document.objects.values('status').annotate(num_docs = Count('status'))
    
    chart3 = [
        ['Status', 'Count'],
    ]
    for i in range(0, statusDoc.count()):
        chart3.append([statusDoc[i]['status'], statusDoc[i]['num_docs']])
    
    assignDoc = Assignment.objects.values('process_emp_id').annotate(num_docs = Count('status')).filter(status__in = ['Processed','Under Review','Reviewed'])
    
    chart4 = [
        ['Employee ID', 'Min Threshold', 'Document Processed'],
    ]
    for i in range(0, assignDoc.count()):
        chart4.append([assignDoc[i]['process_emp_id'], 8, assignDoc[i]['num_docs']])
        
    # docTime = Document.objects.values('doc_id','time_to_process','time_to_review','total_time').exclude(status__in = ['Assigned','Under Process'])
    docTime = Document.objects.values('doc_id','time_to_process','time_to_review','total_time').filter(status = 'Reviewed')
    chart5 = [['Document','Process Time','Review Time','Total Time']]
    for i in range(0, docTime.count()):
        processTime = 0 if pd.isna(pd.Timedelta(docTime[i]['time_to_process'])) else pd.Timedelta(docTime[i]['time_to_process']).total_seconds() / 60
        reviewTime = 0 if pd.isna(pd.Timedelta(docTime[i]['time_to_review'])) else pd.Timedelta(docTime[i]['time_to_review']).total_seconds() / 60
        totalTime = 0 if pd.isna(pd.Timedelta(docTime[i]['total_time'])) else pd.Timedelta(docTime[i]['total_time']).total_seconds() / 60
        # reviewTime = pd.Timedelta(docTime[i]['time_to_review'])
        # totalTime = pd.Timedelta(docTime[i]['total_time'])
            
        chart5.append([docTime[i]['doc_id'],int(str(int(processTime))[:4]),int(str(int(reviewTime))[:4]),int(str(int(totalTime))[:4])])
    
    
    return Response({"chart1":chart1, "chart2":chart2, "chart3": chart3, "chart4": chart4, "chart5":chart5})
            
    
    
    
    
# Assignment.objects.values('process_emp_id').annotate(num_docs = Count("doc_id"))
# <QuerySet [{'process_emp_id': 'EmpOne', 'num_docs': 11}, {'process_emp_id': 'EmpThree', 'num_docs': 11}, {'process_emp_id': 'EmpTwo', 'num_docs': 10}]>

# Document.objects.values('doc_id').filter(type='Balance Sheet')
# Assignment.objects.values('process_emp_id').annotate(num_docs = Count('doc_id')).filter(doc_id__in = doc1)
# <QuerySet [{'process_emp_id': 'EmpOne', 'num_docs': 4}, {'process_emp_id': 'EmpThree', 'num_docs': 5}, {'process_emp_id': 'EmpTwo', 'num_docs': 3}]>

# Document.objects.values('status').annotate(num_docs = Count('status'))
# <QuerySet [{'status': 'Assigned', 'num_docs': 5}, {'status': 'Processed', 'num_docs': 6}, {'status': 'Reviewed', 'num_docs': 12}, {'status': 'Under Process', 'num_docs': 3}, {'status': 'Under Review', 'num_docs': 6}]>

# doc2 = Assignment.objects.values('status').annotate(num_of_docs=Count('status')).filter(status__in=['Processed','Under Review','Reviewed'])
# <QuerySet [{'status': 'Processed', 'num_of_docs': 6}, {'status': 'Reviewed', 'num_of_docs': 12}, {'status': 'Under Review', 'num_of_docs': 6}]>

# Assignment.objects.values('process_emp').annotate(num_of_docs=Count('status')).filter(status__in=['Processed','Under Review','Reviewed'])
# <QuerySet [{'process_emp': 'EmpOne', 'num_of_docs': 9}, {'process_emp': 'EmpThree', 'num_of_docs': 8}, {'process_emp': 'EmpTwo', 'num_of_docs': 7}]>


