import React, { useState } from 'react'
import logo from '../assets/logo-mobile.svg'
import iconDown from '../assets/icon-chevron-down.svg'
import iconup from '../assets/icon-chevron-up.svg'
import AddEditTaskModal from '../modals/AddEditTaskModal'

function Header() {
        
    const [openAddEditTask, setOpenAddEditTask] = useState(false)

    return (
        <div className=' p-4 fixed left-0 bg-[#2b2c37] z-50 right-0'>

            <header className=' flex justify-between text-white items-center'>
                
                {/* Left Side */}

                <div className=' flex items-center space-x-2 md:space-x-4 '>
                    <img src={logo} alt='logo' className=' h-6 w-6 '/>
                    <h3 className=' hidden md:inline-block font-bold font-sans md:text-4xl'>
                        Task Board
                    </h3>
                    {/* <div>
                        <h3 className=' truncate max-w-[200px] md:text-2xl text-xl font-bold md:ml-20 font-sans'>
                            board Name
                        </h3>
                    </div> */}
                </div>

                {/* Right Side */}

                <div className='flex space-x-4 items-center md:space-x-6'>
                    <button
                    onClick={
                        () => {
                            setOpenAddEditTask(state => !state)
                        }
                    }
                    className=' hidden md:block button'>
                        + Add New Document
                    </button>

                    <button
                    onClick={
                        () => {
                            setOpenAddEditTask(state => !state)
                        }
                    }
                    className=' button py-1 px-3 md:hidden'>
                        +
                    </button>
                </div>
            </header>
            
            {
                openAddEditTask && <AddEditTaskModal setOpenAddEditTask={setOpenAddEditTask} type="add"/>
            }

        </div>
    )
}

export default Header