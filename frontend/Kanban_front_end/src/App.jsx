import React, { useEffect } from 'react'
import Header from './components/Header'
import Center from './components/Center'
import { useDispatch } from 'react-redux'
import { fetchData } from './redux/boardsSlice'
import Dashboard from './components/Dashboard'
import Charts from './components/Charts'



function App() {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(fetchData())
  }, [])
  return (
    <div>
    
    {/* Header Section */}

    <Header/>

    {/* Center Section */}

    <Center />

    {/* DashBoard Header Section */}

    <Dashboard />

    {/* Dashboard Charts */}

    <Charts />

    </div>
  )
}

export default App