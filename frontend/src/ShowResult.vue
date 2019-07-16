<style rel="stylesheet/scss" lang="scss" scoped>
.main {
  bottom: 0;
  height: 100%;
}
</style>
<template>
  <div id="main">
    <div>
      <el-button type="primary" @click="export_file()">导出</el-button>

  <el-table :data="tableData" v-loading="loading" :element-loading-text="loading_text" border style="width: 100%">
    <el-table-column v-for="(item, index) in column_list" :key="index" :prop="item" :label="item"></el-table-column>
  </el-table>
    </div>
  <el-button-group >
    <el-button type="primary" icon="el-icon-arrow-left" @click="prePage()">上一页</el-button>
    <el-button type="primary" @click="nextPage()">下一页<i class="el-icon-arrow-right el-icon--right"></i></el-button>
  </el-button-group>
  </div>
</template>

<script>
import axios from "axios";
import qs from 'qs'
export default {
  data() {
    return {
      operation: '',
      loading: true,
      loading_text: '',
      column_list: [],
      tableData: [
      ],
      post_data: {
        ids: [
          0,
          1
        ],
        start: 2,
        num: 20
      }
    };
  },
  methods: {
    funnel(start, num) {
      if (start != undefined){
        this.post_data.start = start;
      }
      if (num != undefined){
        this.post_data.num = num;
      }
      var that = this;
      axios.post("http://127.0.0.1:5000/funnel", this.post_data)
        .then(function(response) {
          that.load_data(response.data)
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    diff(start, num) {
      if (start != undefined){
        this.post_data.start = start;
      }
      if (num != undefined){
        this.post_data.num = num;
      }
      var that = this;
      axios.post("http://127.0.0.1:5000/diff", this.post_data)
        .then(function(response) {
          that.load_data(response.data)
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    load_data(data){
      var column_list = data.column_list;
      this.column_list = column_list;
      this.tableData = data['data'];
      this.loading = false;
    },
    prePage(){
      var num = this.post_data.num;
      var start = this.post_data.start - num;
      if (start < 0) {
        start = 0;
      }
      if(this.operation === 'funnel'){
        this.funnel(start, num);
      }else if(this.operation === 'diff'){
        this.diff(start, num);
      }
    },
    nextPage(){
      var num = this.post_data.num;
      var start = this.post_data.start + num;
      if(this.operation === 'funnel'){
        this.funnel(start, num);
      }else if(this.operation === 'diff'){
        this.diff(start, num);
      }
    },
    export_file: function () {
      var that = this;
      const dialog = require('electron').remote.dialog
      dialog.showSaveDialog({
        title: '导出到',
        defaultPath: this.operation + '.xlsx',
      }, (filename => {
        if (filename === undefined) {
          return;
        }
        that.loading = true;
        that.loading_text = '正在导出';
        axios.post('http://127.0.0.1:5000/export', {
          path: filename,
          operation: this.operation,

          a: Math.round(Math.random() * 1000) // 防止文件无更新
        }, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
          },
          transformRequest: [function (data) {
            return qs.stringify(data)
          }]
        }).then(function (response) {
          var data = response.data
          if (data === 'success') {
            that.loading = false;
            alert('success')
          } else {
            that.loading = false;
            alert('error')
          }
        })
      }));
    }
  },
  mounted: function(){
    if(this.operation === 'funnel'){
      this.funnel();
    }else if(this.operation === 'diff'){
      this.diff();
    }
  }
};
</script>