import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import TaskModal from '../modals/TaskModal'
import ReCheckModal from '../modals/ReCheckModal';

function Task({taskIndex, colIndex}) {

    const columns = useSelector(state => state.boards.board.columns)
    const col = columns.find((col, i) => i === colIndex)
    const task = col.tasks.find((task, i) => i === taskIndex)

    const [isTaskModalOpen, setIsTaskModalOpen] = useState(false)
    const [isReCheckModal, setIsReCheckModal] = useState(false)
    const [comments, setComments] = useState("")

    const reCheckChange = (e) => {
        setIsReCheckModal(true)   
        setIsTaskModalOpen(false)
      }

    const handleOnDrag = (e) => {
        e.dataTransfer.setData(
          "text",
          JSON.stringify({ taskIndex, prevColIndex: colIndex })
        );
    };

    const onRecheckBtnClick = (e) => {
        if(e.target.textContent == 'Re-check'){
          let payload = {
            comment: task.empId+": "+comments,
            docId: task.Id
          }
          console.log(payload)
        }else{
          setIsTaskModalOpen(true)
        }
        // setChecked(!checked)
        setComments("")
        setIsReCheckModal(false)
    }

    return (
        <div>
            <div
            onDragStart={handleOnDrag}
            draggable
            onClick={() => { setIsTaskModalOpen(true);}}
            className=" w-[280px] first:my-5 rounded-lg  bg-white  dark:bg-[#2b2c37] shadow-[#364e7e1a] py-6 px-3 shadow-lg hover:text-[#635fc7] dark:text-white dark:hover:text-[#635fc7] cursor-pointer "
            >
                <p className=" font-bold tracking-wide ">
                    {task.title}
                </p>
                <p className=" font-bold text-xs tracking-tighter mt-2 text-gray-500">
                Assigned to {task.empId}
                </p>
            </div>
            {
                isTaskModalOpen && (
                    <TaskModal
                    colIndex={colIndex}
                    taskIndex={taskIndex}
                    setIsTaskModalOpen={setIsTaskModalOpen}
                    reCheckChange={reCheckChange}
                    />
                )
            }
            { isReCheckModal && 
                <ReCheckModal 
                    setIsReCheckModal={setIsReCheckModal}
                    taskId = {task.Id}
                    setIsTaskModalOpen={setIsTaskModalOpen}
                    onRecheckBtnClick = {onRecheckBtnClick}
                    comments = {comments}
                    setComments = {setComments}
                />
            }
    </div>
    )
}

export default Task