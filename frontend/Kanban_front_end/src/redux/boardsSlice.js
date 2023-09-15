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

export const chartData = createAsyncThunk(
    'chartData',
    async () => {
        const res = await fetch('http://127.0.0.1:8000/api/dashBoard')
        const data = await res.json()
        return data;
    }
)

export const addDoc = createAsyncThunk(
    'addDoc',
    async (payload) => {
        console.log("In Add Doc", payload)
        const res = await fetch('http://localhost:8000/api/docs',{
            method: 'POST',
            headers: {
                "content-type": "application/json",
            },
            body: JSON.stringify(payload)
        })
        console.log(res, "Before JSON")
        const data = await res.json();
        console.log(data)
        return data;
    }
)

export const updateDoc = createAsyncThunk(
    'updateDoc',
    async(payload) => {
        console.log(payload)
        const res = await fetch(`http://127.0.0.1:8000/api/docDetails/${payload.Id}`,{
            method: 'POST',
            headers: {
                "content-type": "application/json",
            },
            body: JSON.stringify(payload.data)
        })
        const data = await res.json();
        console.log(data)
        let finalres = {
            "data":data,
            "colIndex": payload.colIndex,
            "taskIndex": payload.taskIndex,
            "drag": payload.drag
        }
        console.log(finalres)
        return finalres;
    }
)

const boardsSlice = createSlice({
    name: 'boards',
    initialState: {
        isLoading: false,
        isError: false,
        board: {
            "columns":[]
        },
        chart: {
            isLoading: false,
            isError: false,
            chart: {
                "data": []
            }
        }
    },
    reducers: {
        addTask: (state, action) => {
            console.log("Here",state)
            const { newColIndex, data } = action.payload
            const column = state.board.columns.find((col, index) => index === newColIndex)
            console.log(column)
            column.task.push({
                data
            })
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
            console.log("Fulfilled",action.payload);
            const col = state.board.columns[0]
            console.log(col)
            const data = action.payload['data']
            col.tasks.push(data)
        })
        builder.addCase(addDoc.rejected, (state, action) => {
            console.log("Rejected", action);
        })
        builder.addCase(updateDoc.pending, (state, action) => {
            console.log("pending");
        })
        builder.addCase(updateDoc.fulfilled, (state, action) => {
            console.log("Fulfilled",action.payload);
            // const { colIndex, prevColIndex, taskIndex } = action.payload;
            const board = state.board
            const prevCol = board.columns.find((col, i) => i === action.payload['colIndex']-1);
            if(action.payload['drag']){
                const task = prevCol.tasks.splice(action.payload['taskIndex'], 1)[0];
                console.log(action.payload['data']['data'])
                board.columns.find((col, i) => i === action.payload['colIndex']).tasks.push(action.payload['data']['data']);
            }else{
                const col = state.board.columns.find((col, i) => i === action.payload['colIndex']-1);
                const task = col.tasks.find((task, i) => i === action.payload['taskIndex']);
                task.status = action.payload['data']['data']['status'];
                col.tasks = col.tasks.filter((task, i) => i !== action.payload['taskIndex']);
                const newCol = state.board.columns.find((col, i) => i === action.payload['colIndex']);
                newCol.tasks.push(task);
            }
            
        })
        builder.addCase(updateDoc.rejected, (state, action) => {
            console.log("Rejected", action);
        })

        builder.addCase(chartData.pending, (state, action) => {
            state.chart.isLoading = true;
            console.log("pending");
        })
        builder.addCase(chartData.fulfilled, (state, action) => {
            state.chart.isLoading = false;
            state.chart.chart.data = action.payload
            console.log("Got the data");
        })
        builder.addCase(chartData.rejected, (state, action) => {
            state.chart.isLoading = false;
            state.chart.isError = true;
            console.log("Rejected", action);
        })
    }
})

export default boardsSlice;