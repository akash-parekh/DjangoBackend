// import { useState } from 'react'
import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import  {shuffle}  from "lodash"
import Task from './Task'
import boardsSlice, { updateDoc } from '../redux/boardsSlice'

function Column({ colIndex}) {

    const dispatch = useDispatch()
    
    const colors = [
        'bg-red-500',
        'bg-orange-500',
        'bg-blue-500',
        'bg-purple-500',
        'bg-green-500',
        'bg-indigo-500',
        'bg-yellow-500',
        'bg-sky-500',
    ]

    const [color, setColor] = useState(null)
    const board = useSelector(state => state.boards.board)
    const col = board.columns.find((col, i) => i === colIndex)
    
    // const task = col.tasks.find((task, i) => i === taskIndex)

    useEffect(() => {
        setColor( shuffle(colors).pop())
    }, [dispatch])
    
    const handleOnDrop = (e) => {
        const { prevColIndex, taskIndex } = JSON.parse(
          e.dataTransfer.getData("text")
        );
    
        if (colIndex == prevColIndex+1) {
          const task = board.columns.find((col, i) => i === prevColIndex)
          // console.log(task.tasks[taskIndex].Id)
          let name = col.name == 'Completed' ? 'Reviewed' : col.name
          let payload = {
            "data":{
              "status": name
            },
            "taskIndex": taskIndex,
            "colIndex": colIndex,
            "Id": task.tasks[taskIndex].Id,
            "drag": true
          }
          console.log(payload)
          // dispatch(
          //   boardsSlice.actions.dragTask({ colIndex, prevColIndex, taskIndex })
          // );
          dispatch(updateDoc(payload))
        }
      };
    
    const handleOnDragOver = (e) => {
    e.preventDefault();
    };

    return (
        <div
        onDrop={handleOnDrop}
        onDragOver={handleOnDragOver}
        className="scrollbar-hide mx-5 pt-[90px] min-w-[280px]"
        >
            <p className=" font-semibold flex  items-center  gap-2 tracking-widest md:tracking-[.2em] text-[#828fa3]">
                <div className={`rounded-full w-4 h-4 ${color} `} />
                   {col.name} ({col.tasks.length})
            </p>

            {
                col.tasks.map((task, index) => (
                    <Task key={index} taskIndex={index} colIndex={colIndex} />
                ))
            }
        </div>
    )
}

export default Column