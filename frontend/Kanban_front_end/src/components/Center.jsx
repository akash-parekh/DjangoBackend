import React from 'react'
import { useSelector } from 'react-redux'
import Column from './Column'

function Center() {

  const columns = useSelector((state) => state.boards.board.columns)

  return (
    <div
    className='bg-[#f4f7fd] scrollbar-hide h-screen flex dark:bg-[#20212c] overflow-x-scroll gap-6'
    >
      {/* Column Section */}
      {
        columns.map((col, index) => (
          <Column key={index} colIndex={index} />
        )
      )}
    </div>
  )
}

export default Center