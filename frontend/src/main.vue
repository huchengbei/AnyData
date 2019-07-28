<style>
  html, body, .container, .homeBox  {
      height: 100%;
      overflow-y: hidden;
  }

  .main {
    height: 100%;
  }

  section{
      height: 100%;
  }

  .homeBox > .el-container >.el-header, .homeBox > .el-container > .el-container > .el-container > .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    padding-top: 5%;
    padding-bottom: 5%;
    /* line-height: 200px; */
  }

  .el-main {
    /* background-color: #E9EEF3; */
    color: #333;
    /* text-align: center; */
    /* line-height: 160px; */
  }

  body > .el-container {
    margin-top: 0%;
    height: 100%;
    /* margin-bottom: 40px; */
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
<template>
  <div class="homeBox">
    <el-container>
        <el-header style="margin-bottom:30px; weight:1200; height:60px; background-image: url(static/images/header_bg.png);"></el-header>
        <el-container>
            <el-header height="30px" >
                <el-breadcrumb separator-class="el-icon-arrow-right" style="font-size:15px;">
                    <el-breadcrumb-item><span v-html="step_one_label" @click="toStep(1)"></span></el-breadcrumb-item>
                    <el-breadcrumb-item><span v-html="step_two_label" @click="toStep(2)"></span></el-breadcrumb-item>
                    <el-breadcrumb-item><span v-html="step_three_label" @click="toStep(3)"></span></el-breadcrumb-item>
                    <el-breadcrumb-item><span v-html="step_four_label" @click="toStep(4)"></span></el-breadcrumb-item>
                </el-breadcrumb>
            </el-header>
            <el-container>
                <el-main>
                    <div id='main'></div>
                </el-main>
                <el-footer v-if="step != 4 && step != 2" style="background: white; margin-bottom: 50px;">
                    <el-button type="primary" @click="nextStep()">下一步</el-button>
                </el-footer>
            </el-container>
        </el-container>
    </el-container>
  </div>
</template>

<script>
import Vue from 'vue';
import ElementUI from 'element-ui';
Vue.use(ElementUI)
import ChooseFile from './ChooseFile';
import ChooseOperation from './ChooseOperation';
import ChooseTable from './ChooseTable';
import ShowResult from './ShowResult.vue';
import Charts from './Charts.vue';
export default {
    name: 'main',
    data() {
      return {
        files: [],
        header: '易分析',
        step_one_label: '',
        step_two_label: '',
        step_three_label: '',
        step_four_label: '',
        step: 1,
        operation: '',
        chooseFile: '',
        chooseOperation: '',
        chooseTable: '',
        showResult: '',
        charts: '',
      }
    },
    methods: {
        nextStep(){
            if(this.step === 1) {
                if(this.chooseFile.check()){
                  this.files = this.chooseFile.tableData;
                  this.mountChooseOperation();
                  // this.mountCharts();
                }
            }else if(this.step === 2) {
              this.operation = this.chooseOperation.operation;
              this.mountChooseTable();
            }else if(this.step === 3) {
              if(this.chooseTable.check_condition()){
                  if(this.operation == 'analyze'){
                      this.mountCharts();
                  }else{
                      this.mountShowResult();
                  }
              }
            }
        },
        toStep(step){
            console.log('this step ' + this.step)
            console.log('step ' + step)
          if (this.step <= step){
              return;
          }
          switch(step){
            case 1:
              this.mountChooseFile();
              break;
            case 2:
              this.mountChooseOperation();
              break;
            case 3:
              this.mountChooseTable();
              break;
          }
        },
        mountChooseFile(){
          this.step_one_label = '<a>选择文件</a>';
          this.step_two_label = '选择操作';
          this.step_three_label = '选择表格';
          this.step_four_label = '结果';
          this.chooseFile = new Vue(ChooseFile);
          this.chooseFile.tableData = this.files;
          console.log(this.chooseFile.tableData)
          this.chooseFile.$mount('#main')
          this.step = 1;
          console.log(this.step)
        },
        mountChooseOperation(){
          this.step_one_label = '<a>选择文件</a>';
          this.step_two_label = '<a>选择操作</a>';
          this.step_three_label = '选择表格>';
          this.step_four_label = '结果';
          if (this.chooseOperation != ''){
              var chooseOperation = new Vue(ChooseOperation);
              chooseOperation.funnel_hidden = this.chooseOperation.funnel_hidden;
              chooseOperation.diff_hidden = this.chooseOperation.diff_hidden;
              chooseOperation.operation = this.chooseOperation.operation;
              this.chooseOperation = chooseOperation;
          }else{
            this.chooseOperation = new Vue(ChooseOperation);
          }
          this.chooseOperation.parent = this
          this.chooseOperation.$mount('#main')
          this.step = 2;
        },
        mountChooseTable(){
          this.step_one_label = '<a>选择文件</a>';
          this.step_two_label = '<a>选择操作</a>';
          this.step_three_label = '<a>选择表格</a>';
          this.step_four_label = '结果';
          this.chooseTable = new Vue(ChooseTable);
          this.chooseTable.operation = this.chooseOperation.operation;
          this.chooseTable.tables = this.chooseFile.tableData;
          this.chooseTable.$mount('#main')
          this.step = 3;
        },
        mountShowResult(){
          this.step_one_label = '<a>选择文件</a>';
          this.step_two_label = '<a>选择操作</a>';
          this.step_three_label = '<a>选择表格</a>';
          this.step_four_label = '<a>结果</a>';
            this.showResult = new Vue(ShowResult);
            var post_data = {}
            post_data.start = 0;
            post_data.num = 10;
            post_data.main_table_id = this.chooseTable.main_table_id;
            if (this.operation == 'funnel'){
                post_data.condition = this.chooseTable.get_condition();
            }else if (this.operation == 'diff'){
                post_data.ids = this.chooseTable.get_condition();
            }
            this.showResult.post_data = post_data;
            this.showResult.operation = this.chooseOperation.operation;
            this.showResult.$mount('#main')
            this.step = 4;
        },
        mountCharts(){
          this.step_one_label = '<a>选择文件</a>';
          this.step_two_label = '<a>选择操作</a>';
          this.step_three_label = '<a>选择表格</a>';
          this.step_four_label = '<a>分析结果</a>';
          this.charts = new Vue(Charts);
          var obj = this.chooseTable.get_condition();
          this.charts.tables = this.files;
          this.charts.default_id_col['id'] = obj['id'];
          this.charts.default_id_col['col_name'] = obj['col_name'];
          this.charts.$mount('#main')
          this.step = 4;
        },
    },
    mounted() {
      // this.mountCharts();
      this.mountChooseFile();
      // this.mountChooseOperation();
      // this.mountChooseTable();
      // this.mountShowResult();
    }
  }
</script>
