<style rel="stylesheet/scss" lang="scss" scoped>
</style>
<template>
    <div id="main" v-loading="loading" style="height: 100%">
        <div id="left" style="width: 50%;height: 100%;overflow: auto;float: left">
            <div id="pie" v-loading="loading" style="height: 220px; width: 450px">
            </div>
            <div id="bar" v-loading="loading" style="height: 220px; width: 450px">
            </div>
        </div>
        <div id="right" style="width: 50%;height: 100%;overflow: auto;float: right">
            <div>
                <el-select v-model="table_index" placeholder="请选择表格" @change="table_change()">
                    <el-option
                            v-for="(item, index) in tables"
                            :key="index"
                            :label="item.fileName"
                            :value="index">
                    </el-option>
                </el-select>
                <el-select
                        v-model="col_name"
                        style="margin-left: 20px;"
                        placeholder="请选择列"
                        @change="col_change()">
                    <el-option
                            v-for="(item,index) in cols"
                            :key="index"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
            </div>
            <div id="rate" style="height: 220px; width: 450px">
                <el-table
                        :data="rates"
                        style="width: 100%">
                    <el-table-column
                            prop="table_name"
                            label="表名">
                    </el-table-column>
                    <el-table-column
                            prop="total"
                            sortable
                            label="总数">
                    </el-table-column>
                    <el-table-column
                            prop="in"
                            sortable
                            label="在其中数">
                    </el-table-column>
                    <el-table-column
                            prop="pre"
                            sortable
                            label="比例">
                    </el-table-column>
                </el-table>
            </div>
            <div id="table" v-loading="loading" style="height: 220px; width: 450px">
                <el-table
                        :data="datas"
                        border
                        show-summary
                        style="width: 100%">
                    <el-table-column
                            prop="col_name"
                            label="分类">
                    </el-table-column>
                    <el-table-column
                            prop="total"
                            sortable
                            label="数量">
                    </el-table-column>
                    <el-table-column
                            prop="pre"
                            sortable
                            label="比例">
                    </el-table-column>
                </el-table>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    import qs from 'qs'
    export default {
        name: "Charts",
        data() {
            return {
                loading: true,
                rates: [],
                datas: [],
                tables: [],
                table_index: '',
                col_name: '',
                cols: [],
                default_id_col: {}
            }
        },
        methods: {
            table_change(){
                this.cols = this.tables[this.table_index].options;
                this.col_name = '';
            },
            col_change(){
                var id = this.tables[this.table_index].id;
                this.refresh(id, this.col_name);
            },
            refresh(table_id, col_name){
                this.loading = true;
                let echarts = require('echarts/lib/echarts');
                require('echarts/lib/chart/pie');
                require('echarts/lib/chart/bar');
                require('echarts/lib/component/tooltip');
                require('echarts/lib/component/toolbox');
                require('echarts/lib/component/legend');
                require('echarts/lib/component/title');
                let chart_pie = echarts.init(document.getElementById('pie'));
                let chart_bar = echarts.init(document.getElementById('bar'));
                var that = this;
                axios.post('http://127.0.0.1:5000/analyze_table', {
                    id: table_id,
                    col_name: col_name,
                }, {
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
                    },
                    transformRequest: [function(data){
                        return qs.stringify(data)
                    }]
                }).then(function(response) {
                    var data = response.data;
                    chart_pie.setOption(data['pie']);
                    chart_bar.setOption(data['bar']);
                    that.rates = data['rates'];
                    that.datas = data['data_list'];
                    that.loading = false;
                }).catch(function(error){
                    console.log(error)
                })
            }
        },
        mounted: function() {
            this.refresh(this.default_id_col['id'], this.default_id_col['col_name']);
        }
    };
</script>

