import React, { useEffect } from 'react'
import { Chart } from "react-google-charts";
import { useDispatch, useSelector } from 'react-redux';
import { chartData } from '../redux/boardsSlice';


function Charts() {
    const dispatch = useDispatch()
    const chart = useSelector((state) => state.boards.chart.chart)
    
    useEffect(() => {
        dispatch(chartData())
    }, [])
    console.log(chart)
    return (
        <div
        className=' scrollbar-hide  pt-[40px] pl-10 min-w-[280px] dark:bg-[#2b2c37]'
        >
            <div>
                <div
                className=' scrollbar-hide h-screen flex bg-[#20212c] overflow-x-scroll gap-6 pt-4 pl-4'
                >
                    <div>
                        <Chart
                            chartType="ColumnChart"
                            data = {chart.data.chart1}
                            width="450px"
                            height="400px"
                            options={{
                            isStacked:  true,
                            legend: { 
                                position: "top",
                                maxLines: 3,
                                textStyle:{
                                    color: '#fff'
                                },
                                titleTextStyle:{
                                    color: '#fff'
                                }
                            },
                            title: "Document Count by Complexity",
                            titleTextStyle:{
                                color: '#fff'
                            },
                            hAxis: {
                                title: "Employee",
                                textStyle:{
                                    color: '#fff'
                                },
                                titleTextStyle:{
                                    color: '#fff'
                                }
                            },
                            vAxis: {
                                title: "No. of Documents",
                                textStyle:{
                                    color: '#fff'
                                },
                                titleTextStyle:{
                                    color: '#fff'
                                }
                            },
                            backgroundColor: '#2b2c37'
                            }}
                        />
                    </div>

                    <div>
                        <Chart 
                            chartType="PieChart"
                            data = {chart.data.chart3}
                            options={{
                            legend: { 
                                position: "top",
                                maxLines:3,
                                textStyle:{
                                    color: '#fff'
                                }
                            },
                            title: "Document by Status",
                            titleTextStyle:{
                                color: '#fff'
                            },
                            is3D: true,
                            backgroundColor: '#2b2c37'
                            }}
                            width="450px"
                            height="400px"
                        />
                    </div>

                    <div>
                        <Chart
                            chartType="ColumnChart"
                            data = {chart.data.chart2}
                            width="450px"
                            height="400px"
                            options={{
                            isStacked:  true,
                            legend: { 
                                position: "top",
                                maxLines: 3,
                                textStyle:{
                                    color: '#fff'
                                },
                                titleTextStyle:{
                                    color: '#fff'
                                }
                            },
                            title: "Document Count by Type",
                            titleTextStyle:{
                                color: '#fff'
                            },
                            hAxis: {
                                title: "Employee",
                                textStyle:{
                                    color: '#fff'
                                },
                                titleTextStyle:{
                                    color: '#fff'
                                }
                            },
                            vAxis: {
                                title: "No. of Documents",
                                textStyle:{
                                    color: '#fff'
                                },
                                titleTextStyle:{
                                    color: '#fff'
                                }
                            },
                            backgroundColor: '#2b2c37'
                            }}
                        />
                    </div>


                </div>
            </div>
        </div>
    )
}

export default Charts