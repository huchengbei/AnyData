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
    <el-row :gutter="30" v-for="(row,index_r) in tables" :key="index_r">
      <el-col :span="8" v-for="(col,index_c) in row" :key="index_c">
        <el-badge value="√" class="item" type="primary" :hidden="col.hidden">
          <el-card class="grid-content bg-purple">
            <el-button type="info" @click="use_table(col)" style="margin-bottom: 10px">
              <div class="sub-title">{{col.fileName}}</div>
            </el-button>
            <el-radio-group v-if="operation === 'funnel'" v-model="col.in">
              <el-radio
                :disabled="col.hidden"
                v-for="(item, index) in col.radio_options"
                :key="index"
                :label="item.exist"
              >{{item.label}}</el-radio>
            </el-radio-group>
          </el-card>
        </el-badge>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "chooseTable",
  data() {
    return {
      operation: "",
      tables: []
    };
  },
  methods: {
    use_table(item) {
      item.hidden = !item.hidden;
      this.$forceUpdate();
    },
    get_condition() {
      var conditions = [];
      var tables_used = [];
      for (var list of this.tables) {
        for (var table of list) {
          if (!table.hidden){
            tables_used.push(table);
          }
        }
      }
      if (this.operation === "funnel") {
        for (var table of tables_used) {
          conditions.push({
            id: table.id,
            exist: table.in
          });
        }
      } else if (this.operation === "diff") {
        for (var table of tables_used) {
          conditions.push(table.id);
        }
      } else {
        return false;
      }
      return conditions;
    },
    check_condition() {
      var tables_used = [];
      var status = true;
      for (var list of this.tables) {
        for (var table of list) {
          if (!table.hidden){
            tables_used.push(table);
          }
        }
      }
      if (this.operation === 'funnel'){
        if(tables_used.length < 2){
          alert("请至少选择两个表格进行筛选");
          status = false;
          return status;
        }
        for( table of tables_used){
          if (table.in == undefined){
            alert("请对每一个筛选的表格确定是否需要在其中");
            status = false;
            return status;
          }
        }
      }else if (this.operation === 'diff'){
        if(tables_used.length != 2){
          alert("请选择两个表格进行对比");
          status = false;
          return status;
        }
      }
      return true;
    },
  },
  beforeMount() {
    for (var i in this.tables) {
      for (var j in this.tables[i]) {
        this.tables[i][j].hidden = true;
        this.tables[i][j].radio_options = [
          {
            exist: 1,
            label: "在其中"
          },
          {
            exist: 0,
            label: "不在其中"
          }
        ];
      }
    }
  }
};
</script>
