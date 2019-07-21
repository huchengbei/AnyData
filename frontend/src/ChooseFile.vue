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
    </div>
  <div class="file-container">
    <div class="file-selecter">
      <!-- el-input -->
      <el-input placeholder="点击左侧图标选择文件,仅支持.xls或.xlsx文件" v-model="fileSelected" :disabled="true">
        <template slot="prepend">
          <el-button type="primary" @click="showOpenDialog()"><i style="color:#409EFF" class="el-icon-upload"></i></el-button>
        </template>
      </el-input>
    </div>
    <div class="file-datatable">
      <div>
        <label>共对 {{tableData.length}} 个表格进行操作</label>
        <el-button type="danger" style="float: right; padding: 7px 2px" @click="reset">
          清除所有<i class="el-icon-delete-solid"></i>
        </el-button>
      </div>
      <el-table v-loading="isLoading"
                element-loading-text="拼命加载中"
                :data="tableData"
                :default-sort = "{prop: 'filePath', order: 'descending'}"
                stripe
                style="width: 100%">
        <el-table-column prop="filePath"
                         label="文件路径"
                         fixed >
        </el-table-column>
        <el-table-column prop="main_key"
                         label="主Key"
                         width="200">
          <template slot-scope="scope">
              <div v-if="scope.row.loading" align="center" style="font-size: 20px" >
                <i class="el-icon-loading is-big"></i>
              </div>
          <el-select v-else v-model="scope.row.main_key"placeholder="点击选择主键" :loading="scope.row.loading"
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
        <el-table-column prop="fileSize"
                         label="文件大小"
                         width="100">
        </el-table-column>
        <el-table-column label="操作"
                         fixed="right"
                         width="100">
          <template slot-scope="scope">
            <el-button type="danger" @click="removeRow(scope.row)" icon="el-icon-delete" circle></el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
  </el-card>
</div>
</template>

<script>
import axios from 'axios'
import qs from 'qs'
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
        if(confirm('是否确定全部清除？')) {
          axios.post('http://127.0.0.1:5000/reset' ).then(function(response) {
            if (response.data == "success"){
              that.tableData = []
            }
          }).catch(function(error){
            console.log(error)
          })
        }
      },
      check_main_key() {
        var status = true;
        for (var item of this.tableData){
          status &= item.main_key_setted;
        }
        return status;
      },
      removeRow(data) {
        if(confirm('是否确定删除此项？')) {
          this.tableData.splice(this.tableData.indexOf(data), 1);
        }
      },
    }
  }
</script>
