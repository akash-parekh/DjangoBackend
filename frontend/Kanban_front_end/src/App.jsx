import React, { useEffect } from 'react'
import Header from './components/Header'
import Center from './components/Center'
import { useDispatch } from 'react-redux'
import { fetchData } from './redux/boardsSlice'



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

    </div>
  )
}

export default App