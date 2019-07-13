<style rel="stylesheet/scss" lang="scss" scoped>
.main {
  bottom: 0;
}
</style>
<template>
  <div id="main">
  <el-table :data="tableData" v-loading="loading" border style="width: 100%">
    <el-table-column v-for="(item, index) in column_list" :key="index" :prop="item" :label="item"></el-table-column>
  </el-table>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      optration: '',
      loading: true,
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
          var response_data = response.data;
          var column_list = response_data.column_list;
          that.column_list = column_list;
          that.tableData = response_data['data'];
          that.loading = false;
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    diff(start, num) {
      console.log(this.post_data);
      if (start != undefined){
        this.post_data.start = start;
      }
      if (num != undefined){
        this.post_data.num = num;
      }
      var that = this;
      axios.post("http://127.0.0.1:5000/diff", this.post_data)
        .then(function(response) {
          var response_data = response.data;
          var column_list = response_data.column_list;
          that.column_list = column_list;
          that.tableData = response_data['data'];
          that.loading = false;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  },
  mounted: function(){
    if(this.optration === 'funnel'){
      this.funnel();
    }else if(this.optration === 'diff'){
      this.diff();
    }
  }
};
</script>