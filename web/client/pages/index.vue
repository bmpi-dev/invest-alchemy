<template>
  <Row type="flex" justify="center">
    <Col span="18">
      <div class="content">
          <div class="title"><h1>ETF双均线策略交易信号订阅</h1></div>
          <div>
            <Input class="email" v-model="email" placeholder="Email" />
            <Button v-on:click="subscribe()" type="primary">Subscribe</Button>
            <Alert class="message" v-if=this.subscribe_message_show type="success">订阅成功，请去邮箱确认订阅吧！(邮件标题为：AWS Notification - Subscription Confirmation)</Alert>
            <Alert class="message" v-if=this.error_message_show type="error">{{this.error_message}}</Alert>
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

  .email {
    margin: 10px 0;
  }

  .message {
    margin-top: 10px;
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
      email: null,
      subscribe_message_show: false,
      error_message: "",
      error_message_show: false,
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
    },

    subscribe: function() {
      if (this.email != null && this.email != "") {
        this.$Message.info({
                content: "正在请求...",
                duration: 3
            });
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email })
        };
        fetch("https://fey17sm0g7.execute-api.us-east-1.amazonaws.com/dev/subscribe", requestOptions)
        .then(response => response.json())
        .then(data => {
          const r = JSON.parse(data);
          const body = JSON.parse(r.body);
          if (body.code == 0) {
            this.subscribe_message_show = true;
            this.error_message_show = false;
            this.error_message = "";
          } else {
            this.subscribe_message_show = false;
            this.error_message_show = true;
            this.error_message = body.message;
          }
        });
      } else {
        this.$Message.info({
                content: "请填写邮箱！",
                duration: 3
            });
      }
    }
  }
};
</script>