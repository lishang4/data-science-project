<template>
  <div>
      <div>
        <div>
          <span class="total">標題</span>
        </div>
      </div>

      
      <div id="tag-content">
        <div id="search-filter">
          <div>
            <div>
              <div>股票代碼</div>
              <div>
                <el-input size="mini" v-model="searchStockCode"></el-input>
              </div>
            </div>
          </div>
          <div>
            <el-button size="mini" type="primary" @click="getStocksList()" >
              {{"搜尋"}}
            </el-button>
            <el-button size="mini" @click="resetFilter()">
              {{"重置"}}
            </el-button>
          </div>
        </div>

        <div id="content">
          <div id="table-block">
            <el-table id="qi-tag-table"
              :data="tableData"
              @selection-change="handleCheckedChange"
              height="100%">
              <el-table-column v-if="canEdit"
                type="selection"
                width="55">
              </el-table-column>
              <template v-for="header in tableHeader">
                <el-table-column 
                  :key="header.keys"
                  :label="header.text"
                  :width="header.width"
                  :fixed="header.fixed || false">
                </el-table-column>
              </template>

              <div v-if="zeroSearchResult"  class="empty-msg" slot="empty">
                <div>查無結果</div>
              </div>
              <div v-else-if="totalCount === 0" class="empty-msg" slot="empty">
                <div>沒有資料</div>
              </div>

            </el-table>
          </div>
        </div>
      </div>
  </div>
</template>
<script>
import { mapMutations } from 'vuex';
import api from './components/stocks';

export default {
  api,
  
  data() {
    return {

      totalCount: 0,
      searchStockCode: '',
      zeroSearchResult: false,

      checkedStocks: [],
      isTableLoading: false,

      tableHeader: [
        {
          key: 'Date',
          text: 'Date',
          width: '100',
        },
        {
          key: 'Capacity',
          text: 'Capacity',
          minWidth: '100',
        },
        {
          key: 'Transaction',
          text: 'Transaction',
          minWidth: '100',
        },
        {
          key: 'Turnover',
          text: 'Turnover',
          minWidth: '100',
        },
        {
          key: 'Open',
          text: 'Open',
          minWidth: '100',
        },
        {
          key: 'High',
          text: 'High',
          minWidth: '100',
        },
        {
          key: 'Low',
          text: 'Low',
          minWidth: '100',
        },
        {
          key: 'Close',
          text: 'Close',
          minWidth: '100',
        },
        {
          key: 'Change',
          text: 'Change',
          minWidth: '100',
        },
      ],

      tableData: [],

      hintTooltip: {
        msg: this.$t('emotivoice.qi_comparison.comparison_hint'),
      },

      // pop window
      editComparisonPopData: undefined,
      isShowEditComparisonPop: false,
      handleValidateSuccess: () => {},
    };
  },
  computed: {
  },
  methods: {
    ...mapMutations([
      'setStocksList',
    ]),
    handleCheckedChange(checkedData) {
      this.checkedStocks = checkedData;
    },
    getStocksList() {
      const that = this;
      that.$api.getStocksList(undefined)
        .then((response) => {
          that.totalCount = response.paging.total;
          that.tableData = that.formatTableData(response.data);
          that.setStocksList(response.data);
        })
        .catch((error) => {
          console.error({ error });
          that.totalCount = 0;
          that.tableData = [];
          that.$msgError('failed');
        });
    },
    formatTableData(comparisons) {
      return comparisons.map((comparison) => {
        comparison.comparison_type = this.parseComparisonTypeWording(comparison.type);
        comparison.actions = [{
          text: this.$t('general.edit'),
          type: 'edit',
          onclick: this.popEditComparison,
        }];
        return comparison;
      });
    },
    resetFilter() {
      const that = this;
      that.searchStockCode = '';
      that.getStocksList();
    },
  },

  mounted() {
    const that = this;
    that.getStocksList();
  },
};
</script>
<style lang="scss" scoped>

.table-block {
  flex: 1;
  display: flex;
  overflow: hidden;
}
.import-tool {
  display: flex;
  align-items: center;
  .fileChooser {
    display: none;
  }
}
.import-block {
  background: #FF1111;
  border-radius: 4px;
  padding: 10px 16px;
  margin: 10px;
  .title {
    color: #121212;
    display: flex;
  }
  .tools {
    margin-top: 10px;
    .hint {
      margin-bottom: 10px;
    }
    .el-button {
      height: 1000px;
      width: 100%;
    }
  }
}
</style>
