import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
// import  from 'axios';


export const fetchData = createAsyncThunk(
    'fetchData',
    async () => {
        console.log("In Fetch")
        const res = await fetch('http://localhost:8000/api/boardData')
        const data = await res.json();
        return data;
    }
)

export const addDoc = createAsyncThunk(
    'addDoc',
    async ({payload}) => {
        console.log("In Add Doc")
        const res = await fetch('http://localhost:8000/api/docs',{
            method: 'POST',
            headers: {
                "content-type": "application/json",
            },
            body: payload
        })
        const data = await res.json();
        return data;
    }
)

const boardsSlice = createSlice({
    name: 'boards',
    initialState: {
        isLoading: false,
        isError: false,
        board: {
            "columns":[]
        }
    },
    reducers: {
        addTask: (state, action) => {
            console.log("Here",state)
            const { doc_name , doc_id, type, complexity, newColIndex } = action.payload;
            const column = state.board.columns.find((col, index) => index === newColIndex)
            let payload = {
                "doc_name": doc_name,
                "doc_id": doc_id,
                "type": type,
                "complexity": complexity
            }
            console.log("Payload - ",payload)
            // const res = addDoc(payload)
            // if(res['Message']) column.tasks.push(res.data)
            // else console.log("Error Occurred")
        },
        dragTask: (state, action) => {
            const { colIndex, prevColIndex, taskIndex } = action.payload;
            const board = state.board
            const prevCol = board.columns.find((col, i) => i === prevColIndex);
            const task = prevCol.tasks.splice(taskIndex, 1)[0];
            board.columns.find((col, i) => i === colIndex).tasks.push(task);
        },
        setTaskStatus: (state, action) => {
            const payload = action.payload;
            const columns = state.board.columns
            // const columns = board.columns;
            const col = columns.find((col, i) => i === payload.colIndex);
            if (payload.colIndex === payload.newColIndex) return;
            const task = col.tasks.find((task, i) => i === payload.taskIndex);
            task.status = payload.status;
            col.tasks = col.tasks.filter((task, i) => i !== payload.taskIndex);
            const newCol = columns.find((col, i) => i === payload.newColIndex);
            newCol.tasks.push(task);
        }
    },
    extraReducers: (builder) => {
        builder.addCase(fetchData.pending, (state, action) => {
            state.isLoading = true;
            console.log("pending");
        })
        builder.addCase(fetchData.fulfilled, (state, action) => {
            state.isLoading = false;
            state.board.columns = action.payload
            console.log(action.payload);
        })
        builder.addCase(fetchData.rejected, (state, action) => {
            state.isLoading = false;
            state.isError = true;
            console.log("Error", action.payload);
        })
        builder.addCase(addDoc.pending, (state, action) => {
            console.log("pending");
        })
        builder.addCase(addDoc.fulfilled, (state, action) => {
            console.log(action.payload);
        })
        builder.addCase(addDoc.rejected, (state, action) => {
            console.log("Error", action.payload);
        })
    }
})

export default boardsSlice;