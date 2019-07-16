<style rel="stylesheet/scss" lang="scss" scoped>
  .file {
    &-selecter {
      padding: 10px;
    }

    &-datatable {
      margin-top: 10px;
    }
  }
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 100%;
  }
</style>
<template>
<div id="main">
  <el-card class="box-card">
    <div class="clearfix">
    <span>请选择需要分析的文件</span>
    <el-button style="float: right; padding: 3px 0" type="text" @click="reset">
      清除所有
    </el-button>
    </div>
  <div class="file-container">
    <div class="file-selecter">
      <!-- el-input -->
      <el-input placeholder="请选择文件,支持多选" v-model="fileSelected" :disabled="true">
        <template slot="prepend">
          <el-button type="primary" @click="showOpenDialog()">选择文件</el-button>
        </template>
      </el-input>
    </div>
    <div class="file-datatable">
      <div>共对 {{tableData.length}} 个表格进行操作</div>
      <el-table v-loading="isLoading" element-loading-text="拼命加载中" :data="tableData" style="width: 100%">
        <el-table-column prop="filePath" label="文件路径"> </el-table-column>
        <el-table-column prop="main_key" label="主Key">
          <template slot-scope="scope">
              <div v-if="scope.row.loading" align="center" style="font-size: 20px" >
                <i class="el-icon-loading is-big"></i>
              </div>
          <el-select v-else v-model="scope.row.main_key"placeholder="请选择" :loading="scope.row.loading"
                     loading-text="正在加载中" @change="select_on_change($event, scope.row)">
            <el-option
              v-for="item in scope.row.options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="fileSize" label="文件大小" fixed="right" width="100"> </el-table-column>
      </el-table>
    </div>
  </div>
  </el-card>
</div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
import { resolve } from 'path';
export default {
    name: 'chooseFile',
    data() {
      return {
        isLoading: false,
        tableData: [],
        temp_status: false
      }
    },
    methods: {
      // 选择文件
      showOpenDialog() {
        const dialog = require('electron').remote.dialog
        dialog.showOpenDialog({
          title: '选择要分析的文件',
          properties: ['openFile']
        }, (filePaths) => {
          const fs = require('fs')
          const path = require('path')
          for (const filePath of filePaths) {
            const stat = fs.statSync(filePath);
            this.tableData.push({
              filePath: filePath,
              fileName: path.basename(filePath),
              fileSize: stat.size,
              options: [],
              loading: true,
              main_key: '',
              id: 0,
              main_key_setted: false
            });
            var that = this;
            axios.post('http://127.0.0.1:5000/load_data', {
              path: filePath
            }, {
              headers: {
                "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
              },
              transformRequest: [function(data){
                return qs.stringify(data)
              }]
            }).then(function(response) {
              var data = response.data;
              var options = [];
              for (var item of data['column_list']){
                options.push({
                  value: item,
                  label: item
                })
              }
              that.tableData[that.tableData.length - 1].options = options;
              that.tableData[that.tableData.length - 1].id = data['id'];
              that.tableData[that.tableData.length - 1].loading = false;
            }).catch(function(error){
              console.log(error)
            })
          }
        })
      },
      select_on_change(event, tableItem) {
        var id = tableItem.id;
        var main_key = event;
        this.set_main_key(id, main_key, tableItem);
      },
      set_main_key(id, main_key, tableItem){
        axios.post('http://127.0.0.1:5000/set_main_key', {
          id: id,
          main_key: main_key
        }, {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
            },
            transformRequest: [function(data){
              return qs.stringify(data)
            }]
        }).then(function(response) {
            if (response.data == "success"){
              // alert("设置成功:" + main_key);
              tableItem.main_key_setted = true;
            }
        }).catch(function(error){
            console.log(error)
            tableItem.main_key_setted = false;
        })
      },
      reset(){
        var that = this;
        axios.post('http://127.0.0.1:5000/reset' ).then(function(response) {
            if (response.data == "success"){
              alert("清除成功");
              that.tableData = []
            }
        }).catch(function(error){
            console.log(error)
        })
      },
      check_main_key() {
        var status = true;
        for (var item of this.tableData){
          status &= item.main_key_setted;
        }
        return status;
      },
    }
  }
</script>
