<style>
  html, body, .container, .homeBox  {
      height: 100%;
      overflow-y: hidden;
  }

  .main {
    height: 100%;
  }

  .homeBox > section{
      height: 100%;
  }

  .el-header, .el-footer {
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
        <el-header>{{header}}</el-header>
        <el-container>
            <el-aside width="20%">
              <div style="height: 100%;overflow-y:hidden;">
              <el-steps direction="vertical" :active="step" >
                <el-step title="选择文件" @click.native="toStep(1)">aaa</el-step>
                <el-step title="选择操作" @click.native="toStep(2)"></el-step>
                <el-step title="选择使用的表格" @click.native="toStep(3)"></el-step>
                <el-step title="结果"></el-step>
              </el-steps>
              </div>
            </el-aside>
            <el-container>
                <el-main>
                    <div id='main'></div>
                </el-main>
                <el-footer>
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
import ChooseOptration from './ChooseOptration';
import ChooseTable from './ChooseTable';
import ShowResult from './ShowResult.vue';
export default {
    name: 'main',
    data() {
      return {
        files: [],
        header: 'Header',
        step: 1,
        optration: '',
        chooseFile: '',
        chooseOptration: '',
        chooseTable: '',
        showResult: '',
      }
    },
    methods: {
        nextStep(){
            if(this.step === 1) {
                if(!this.chooseFile.check_main_key()){
                    alert('请选择main_key');
                }else{
                  this.files = this.chooseFile.tableData;
                  this.mountChooseOptration();
                }
            }else if(this.step === 2) {
              this.optration = this.chooseOptration.optration;
              this.mountChooseTable();
            }else if(this.step === 3) {
              if(this.chooseTable.check_condition()){
                this.mountShowResult();
              }
            }
        },
        toStep(step){
          switch(step){
            case 1:
              this.mountChooseFile();
              break;
            case 2:
              this.mountChooseOptration();
              break;
            case 3:
              this.mountChooseTable();
              break;
          }
        },
        mountChooseFile(){
          this.chooseFile = new Vue(ChooseFile);
          this.chooseFile.tableData = this.files;
          this.chooseFile.$mount('#main')
          this.step = 1;
        },
        mountChooseOptration(){
          if (this.chooseOptration != ''){
              var chooseOptration = new Vue(ChooseOptration);
              chooseOptration.funnel_hidden = this.chooseOptration.funnel_hidden;
              chooseOptration.diff_hidden = this.chooseOptration.diff_hidden;
              chooseOptration.optration = this.chooseOptration.optration;
              this.chooseOptration = chooseOptration;
          }else{
            this.chooseOptration = new Vue(ChooseOptration);
          }
          this.chooseOptration.$mount('#main')
          this.step = 2;
        },
        mountChooseTable(){
          this.chooseTable = new Vue(ChooseTable);
          this.chooseTable.optration = this.chooseOptration.optration;
          var tableData = this.chooseFile.tableData;
          var tables = [];
          var list = [];
          for (var index in tableData){
            if ((index+1) % 3 == 0){
              tables.push(list);
              list = [];
            }
            list.push(tableData[index])
          }
          if (list.length != 0){
              tables.push(list);
          }
          this.chooseTable.tables = tables;
          this.chooseTable.$mount('#main')
          this.step = 3;
        },
        mountShowResult(){
          this.showResult = new Vue(ShowResult);
          var post_data = {}
          post_data.start = 0;
          post_data.num = 10;
          if (this.optration == 'funnel'){
            post_data.condition = this.chooseTable.get_condition();
          }else if (this.optration == 'diff'){
            post_data.ids = this.chooseTable.get_condition();
          }
          this.showResult.post_data = post_data;
          this.showResult.optration = this.chooseOptration.optration;
          this.showResult.$mount('#main')
          this.step = 4;
        },
    },
    mounted() {
      this.mountChooseFile();
      // this.mountChooseOptration();
      // this.mountChooseTable();
      // this.mountShowResult();
    }
  }
</script>
