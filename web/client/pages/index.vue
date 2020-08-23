<template>
  <Row type="flex" justify="center">
    <Col span="12">
      <div class="content">
          <div class="title"><h1>ETF双均线策略交易信号订阅</h1></div>
          <div>
            <Input search enter-button="Subscribe" placeholder="Email" />
          </div>
      </div>

      <div class="history">
        <div class="title"><h1>历史交易信号记录</h1></div>
        <div class="history_content">
          <ul id="v-for-days" class="day">
            <li v-for="day_url in day_urls">
              <a :href=day_url.url>{{day_url.day}}</a>
            </li>
          </ul>
        </div>
      </div>
    </Col>
  </Row>
</template>
<style>
  .title {
    text-align: center;
    margin-bottom: 20px;
  }

  .content {
    margin-top: 20px;
  }

  .history {
    margin-top: 20px;
  }

  .history_content {
    margin: 20px 0;
    font-size: 18px;
    text-align: center;
  }

  .history_content ul {
    list-style: none;
  }
</style>
<script>
export default {
  async asyncData({ store, $http, route }) {
    return { };
  },

  data() {
    return {
      day_urls: [],
    }
  },

  beforeMount(){
    const base_url = 'https://www.i365.tech/invest-alchemy/data/strategy/double-ma/'
    const start_date = new Date('2020-08-22');
    const end_date = new Date();
    const daylist = this.getDaysArray(start_date, end_date);
    this.day_urls = daylist.reverse().map((v)=> {
      return {
        url: base_url + v.toISOString().slice(0,10).replace(/-/g,"") + '.txt', 
        day: v.toISOString().slice(0,10).replace(/-/g,"")
      }
    });
  },

  methods: {
    getDaysArray: function (start, end) {
      for(var arr=[],dt=new Date(start); dt<=end; dt.setDate(dt.getDate()+1)){
          arr.push(new Date(dt));
      }
      return arr;
    }
  }
};
</script>