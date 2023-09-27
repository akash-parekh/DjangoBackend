import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import elipsis from "../assets/icon-vertical-ellipsis.svg";
import ElipsisMenu from "../components/ElipsisMenu";
import { updateDoc } from '../redux/boardsSlice'
function TaskModal({colIndex, taskIndex, setIsTaskModalOpen, reCheckChange}) {
  
  const dispatch = useDispatch()
  const columns = useSelector(state => state.boards.board.columns)
  const col = columns.find((col, i) => i === colIndex)
  const task = col.tasks.find((task, i) => i === taskIndex)

  const [status, setStatus] = useState(task.status)
  const [newColIndex, setNewColIndex] = useState(columns.indexOf(col))

  const onChange = (e) => {
    let index = columns.findIndex((col, i) => col['name'] == e.target.value)
    console.log(e.target.value, index)
    setStatus(e.target.value);
    setNewColIndex(index);
    console.log(colIndex, newColIndex)
  };

  const taskItems = task.documentTrail.map((item) => 
    <li className="pt-2 text-sm">{item}</li>
  );

  // const setOpenEditModal = () => {
  //   setIsAddDocumentModalOpen(true)
  //   setElipsisMenuOpen(false)
  //   // Write
  // }
  
  const onClose = (e) => {
    if(e.target !== e.currentTarget){
      return;
    }
    // setIsTaskModalOpen(false)
    // let newStat = e.target.value 
    let newStat = status
    if(newStat == 'Completed') newStat = 'Reviewed'
    console.log(colIndex, newColIndex)
    if(colIndex == newColIndex){
      setIsTaskModalOpen(false)
      console.log("HERE")
    }else{
      let payload = {
        "data":{
          "status": newStat
        },
        "taskIndex": taskIndex,
        "colIndex": newColIndex,
        "Id": task.Id,
        "drag":false
      }
      dispatch(updateDoc(payload))
      setIsTaskModalOpen(false)
    }
  }

  return (
    <div
    onClick={onClose}
    className=' fixed right-0 left-0 top-0 px-2 py-4 overflow-scroll z-50 bottom-0 justify-center items-center flex bg-[#00000080] scrollbar-hide'
    >
      {/* Modal Section */}
      <div
      className=' overflow-y-scroll scrollbar-hide max-h-[95vh] my-auto bg-white dark:bg-[#2b2c37] text-black dark:text-white font-bold shadow-md shadow-[#364e7e1a] max-w-screen-md mx-auto w-full px-8 py-8 rounded-xl'
      >
        <div
        className=' relative flex justify-between w-full items-start'
        >
          <div>
            <h1
            className='text-lg '
            >
              {task.title}
            </h1>
            <div>
          <p className=" text-gray-500 font-[600] tracking-wide text-sm pt-3">
            <label className=" font-bold">
              Document Id :
            </label>
            <p className="inline-block pt-6"> {task.Id}</p>
          </p>
          <p className=" text-gray-500 font-[600] tracking-wide text-sm">
            <label className=" font-bold">
              Date Added :
            </label>
            <p className="inline-block pt-3">{task.date_added}</p>
          </p>
          <p className=" text-gray-500 font-[600] tracking-wide text-sm">
            <label className=" font-bold">
              Document Type :
            </label>
            <p className="inline-block pt-3">{task.type}</p>
          </p>
          
          <p className=" text-gray-500 font-[600] tracking-wide text-sm">
            <label className=" font-bold">
              Document Complexity :
            </label>
            <p className="inline-block pt-3">{task.complexity}</p>
          </p>

          <p className=" text-gray-500 font-[600] tracking-wide text-sm">
            <label className=" font-bold">
              Employee ID :
            </label>
            <p className="inline-block pt-3">{task.empId}</p>
          </p>
          { columns[colIndex].name == 'Under Review' ?
            <p className=" text-gray-500 font-[600] tracking-wide text-sm pt-3">
                {/* <input
                  className=" w-4 h-4  accent-[#635fc7] cursor-pointer "
                  type="checkbox"
                  checked={checked}
                  onChange={reCheckChange}
                /> */}
                <button className='w-full items-center text-white hover:opacity-75 bg-gray-600 py-2 rounded-full' onClick={reCheckChange}> Re-check </button>
                {/* <label className=' pl-4'>
                  Re-Check
                </label> */}
            </p>

            :
            <>
            </>
          }
          <div className="mt-8 flex flex-col space-y-3">
            <label className="  text-sm dark:text-white text-gray-500">
              Current Status
            </label>
            { columns[colIndex].name == 'Completed' ? 
              <p
              className=' flex-grow px-4 py-2 rounded-md text-sm bg-transparent focus:border-0  border-[1px] border-gray-300 focus:outline-[#635fc7] outline-none'
              >
                {columns[colIndex].name}
              </p>
              :
              <>
                <select
                  className=" select-status flex-grow px-4 py-2 rounded-md text-sm bg-transparent focus:border-0  border-[1px] border-gray-300 focus:outline-[#635fc7] outline-none"
                  value={status}
                  onChange={onChange}
                >
                  {/* {columns.map((col, index) => (
                    <option className="select-status" key={index}>
                      {col.name}
                    </option>
                  ))} */}
                  <option className=" text-white bg-[#2b2c37]" key={colIndex}>
                    {columns[colIndex].name}
                  </option>
                  <option className=" text-white bg-[#2b2c37]" key={colIndex+1}>
                    {columns[colIndex+1].name}
                  </option>
                </select>  
              </>
            }
            
          </div>
          </div>
          </div>
          <div>
            <h1
            className='text-lg '
            >Logs</h1>
            <div className="my-10 h-64 w-72 font-light border-solid border-2 pl-2 border-gray-700 overflow-y-scroll scrollbar-hide">
              <ol>{taskItems}</ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TaskModal