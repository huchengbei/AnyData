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
    <el-row :gutter="30" v-for="(table,index) in tables" :key="index">
        <el-badge value="√" class="item" type="primary" :hidden="table.hidden">
          <el-card class="grid-content bg-purple">
            <el-button type="info" @click="use_table(table)" style="margin-bottom: 10px">
              <div class="sub-title">{{table.fileName}}</div>
            </el-button>
            <el-radio-group v-if="operation === 'funnel'" v-model="table.in">
              <el-radio
                :disabled="table.hidden"
                v-for="(item, index) in table.radio_options"
                :key="index"
                :label="item.exist"
              >{{item.label}}</el-radio>
            </el-radio-group>
            <el-select
                    v-else-if="operation === 'analyze'"
                    :disabled="table.hidden"
                    v-model="table.col_name"
                    style="margin-left: 20px;"
                    placeholder="请选择列"
                    @change="col_change()">
              <el-option
                      v-for="(item,index) in table.options"
                      :key="index"
                      :label="item.label"
                      :value="item.value">
              </el-option>
            </el-select>
          </el-card>
        </el-badge>
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
    col_change() {
      this.$forceUpdate();
    },
    get_condition() {
      var conditions = [];
      var tables_used = [];
      for (var table of this.tables) {
          if (!table.hidden){
            tables_used.push(table);
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
      } else if (this.operation === 'analyze') {
        var id = tables_used[0].id;
        var col_name = tables_used[0].col_name;
        return {
          id: id,
          col_name: col_name
        }
      }else {
        return false;
      }
      return conditions;
    },
    check_condition() {
      var tables_used = [];
      var status = true;
      for (var table of this.tables) {
          if (!table.hidden){
            tables_used.push(table);
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
      }else if (this.operation === 'analyze'){
        if (tables_used.length != 1){
          alert("请仅选择一个表格进行分析");
          status = false;
          return status;
        }
        if (tables_used[0].col_nam == ''){
          alert("请选择分析列");
          status = false;
          return status;
        }
      }
      return true;
    },
  },
  beforeMount() {
    for (var i in this.tables) {
        this.tables[i].hidden = true;
        this.tables[i].col_name = '';
        this.tables[i].radio_options = [
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
};
</script>
