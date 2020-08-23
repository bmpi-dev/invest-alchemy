<template>
  <div>
    <navbar/>
    <nuxt/>
    <div>
      <Row type="flex" justify="center">
        <Col span="12">
          <div class="footer">
            <p>by <a href="https://www.bmpi.dev">BMPI.dev</a></p>
          </div>
        </Col>
      </Row>
    </div>
  </div>
</template>
<script>
import navbar from "~/components/navbar";

export default {
  // components: { navbar }
};
</script>