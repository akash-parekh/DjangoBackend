import React, {useState} from 'react'
import { useDispatch, useSelector } from 'react-redux'
import boardsSlice from '../redux/boardsSlice';

function AddEditTaskModal({ type, setOpenAddEditTask,  prevColIndex = 0, }) {
    const dispatch = useDispatch()
    const columns = useSelector((state) => state.boards.board.columns);
    const col = columns.find((col, index) => index === prevColIndex)
    

    const [title, setTitle] = useState('')
    const [id, setId] = useState('')
    const [doctype, setDocType] = useState('Simple')
    const [complexity, setComplexity] = useState('Balance Sheet')
    const [isValid, setIsValid] = useState(false)
    const [newColIndex, setNewColIndex] = useState(prevColIndex)
    const [status, setStatus] = useState(columns[prevColIndex].name)

    const validate = () => {
        setIsValid(false)
        if(!title.trim()){
            return false
        }
        setIsValid(true)
        return true;
    }

    const onSubmit = () => {
        if(type === 'add'){
            dispatch(
                boardsSlice.actions.addTask({
                    "doc_name":title,
                    "doc_id":id,
                    "type":doctype,
                    "complexity":complexity,
                    newColIndex,
                })
            )
        }
    }

    return (
        <div
        onClick={ (e) => {
            if(e.target !== e.currentTarget){
                return;
            }
            setOpenAddEditTask(false)
        }}
        className=' py-6 px-6 pb-40 absolute overflow-y-scroll left-0 flex right-0 bottom-[-100vh] top-0 bg-[#00000080]'
        >
            {/* Modal Section */}

            <div
            className=' overflow-y-scroll max-h-[95vh] dark:bg-[#2b2c37] dark:text-white font-bold shadow-md shadow-[#364e7e1a] max-w-md mx-auto w-full px-8 py-8 rounded-xl'
            >
                <h3
                className=' text-lg'
                >
                    Add Document
                </h3>
                
                {/* Document Name */}
                <div className=' mt-8 flex flex-col space-y-1'>
                    <label className=' text-sm dark:text-white'>
                        Document Name
                    </label>
                    <input value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className=' bg-transparent px-4 py-2 focus:border-0 rounded-md text-sm border border-gray-600 focus:outline-[#635fc7] ring-0 outline-none'
                    placeholder='e.g Test Document'
                    type='text' />
                </div>

                {/* Document Id */}
                <div className=' mt-8 flex flex-col space-y-1'>
                    <label className=' text-sm dark:text-white'>
                        Document ID
                    </label>
                    <input value={id}
                    onChange={(e) => setId(e.target.value)}
                    className=' bg-transparent px-4 py-2 focus:border-0 rounded-md text-sm border border-gray-600 focus:outline-[#635fc7] ring-0 outline-none'
                    placeholder='e.g TestDoc'
                    type='text' />
                </div>

                {/* Document Type */}
                <div className=' mt-8 flex flex-col space-y-3'>
                    <label className=' text-sm dark:text-white'>
                        Document Type
                    </label>
                    <select
                    value={doctype}
                    onChange={(e) => setDocType(e.target.value)}
                    className=' select-status flex flex-grow px-4 py-2 rounded-md text-sm bg-transparent focus:border-0 border border-gray-300 focus:outline-[#635fc7] outline-none'
                    >
                        <option>Balace Sheet</option>
                        <option>Income Statement</option>
                        <option>Cash Flow Statement</option>
                    </select>
                </div>

                {/* Document Complexity */}
                <div className=' mt-8 flex flex-col space-y-3'>
                    <label className=' text-sm dark:text-white'>
                        Document Complexity
                    </label>
                    <select
                    value={complexity}
                    onChange={(e) => setComplexity(e.target.value)}
                    className=' select-status flex flex-grow px-4 py-2 rounded-md text-sm bg-transparent focus:border-0 border border-gray-300 focus:outline-[#635fc7] outline-none'
                    >
                        <option>Simple</option>
                        <option>Complex</option>
                        <option>Very Complex</option>
                    </select>
                </div>

                {/* Current Status */}
                <div className=' mt-8 flex flex-col space-y-3'>
                    <button
                    onClick={() => {
                        const isValid = validate()
                        if(isValid){
                            onSubmit(type)
                            setOpenAddEditTask(false)
                        }
                    }} 
                    className=' w-full items-center text-white bg-[#635fc7] py-2 rounded-full'
                    >
                        Create Document
                    </button>
                </div>
            </div>
            
        </div>
    )
}

export default AddEditTaskModal