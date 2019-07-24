<style rel="stylesheet/scss" lang="scss" scoped>
  .main {
    align-content: center;
  }
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
<template>
<div id="main" style="margin-top:10%">
<el-row :gutter="30" >
  <el-col :span="8" style="align-content: center;">
    <div>
      <el-button type="primary" style="margin-left:30px; width:250px; height:250px; background-image: url(static/images/funnel.jpg);" plain @click="choose_funnel"></el-button>
    </div>
  </el-col>
  <el-col :span="8">
    <div>
      <el-button type="danger" style="margin-left:30px; width:250px; height:250px; background-image: url(static/images/diff.jpg);" plain @click="choose_diff"></el-button>
    </div>
  </el-col>
  <el-col :span="8">
    <div>
      <el-button type="warning" style="margin-left:30px; width:250px; height:250px; background-image: url(static/images/analyze.jpg)" plain @click="choose_analyze"></el-button>
    </div>
  </el-col>
</el-row>
</div>
</template>

<script>
export default {
    name: 'chooseOperation',
    data() {
      return {
        funnel_hidden: true,
        diff_hidden: true,
        analyze_hidden: true,
        operation: '',
     }
    },
    methods: {
      choose_funnel() {
        this.funnel_hidden=false;
        this.diff_hidden=true;
        this.analyze_hidden=true;
        this.operation="funnel";
      },
      choose_diff() {
        this.funnel_hidden=true;
        this.diff_hidden=false;
        this.analyze_hidden=true;
        this.operation="diff";
      },
      choose_analyze() {
        this.funnel_hidden=true;
        this.diff_hidden=true;
        this.analyze_hidden=false;
        this.operation="analyze";
      },
      check_operation(){
        return this.funnel_hidden || this.diff_hidden || this.analyze_hidden;
      }
    }
  }
</script>
