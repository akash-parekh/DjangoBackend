import React from 'react'
import logo from '../assets/logo-mobile.svg'

function Dashboard() {
  return (
    <div className=' p-4 bg-[#2b2c37] z-100'>

        <header className=' flex left-0 justify-between text-white items-center right-0'>
            
            {/* Left Side */}

            <div className=' flex items-center space-x-2 md:space-x-4 '>
                <img src={logo} alt='logo' className=' h-6 w-6 '/>
                <h3 className=' hidden md:inline-block font-bold font-sans md:text-4xl'>
                    DashBoard
                </h3>
            </div>
        </header>
    </div>
  )
}

export default Dashboard