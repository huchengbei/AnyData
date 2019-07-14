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
<div id="main">
<el-row :gutter="30" >
  <el-col :span="8"><div class="grid-content bg-purple">
    <el-badge value="√" class="item" type="primary" :hidden="funnel_hidden">
      <el-button size="big" type="primary" plain @click="choose_funnel">筛选</el-button>
    </el-badge>
    </div></el-col>
  <el-col :span="8"><div class="grid-content bg-purple">
    <el-badge value="√" class="item" type="primary" :hidden="diff_hidden">
      <el-button size="big" type="info" plain @click="choose_diff">对比</el-button>
    </el-badge>
    </div></el-col>
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
        operation: '',
     }
    },
    methods: {
      choose_funnel() {
        this.funnel_hidden=false;
        this.diff_hidden=true;
        this.operation="funnel";
      },
      choose_diff() {
        this.funnel_hidden=true;
        this.diff_hidden=false;
        this.operation="diff";
      },
      check_operation(){
        return this.funnel_hidden || this.diff_hidden;
      }
    }
  }
</script>
