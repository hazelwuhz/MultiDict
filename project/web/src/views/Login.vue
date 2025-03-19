<template>
    <div style="padding-top:10px;">
        <Row style="text-align:center;display:inline;">
            <h1>学生管理系统</h1>
        </Row>
    </div>
    <div style="margin-top:20px;">
        <Row>
            <Col span="8" offset="8">
                <Row>
                    <Col span="4"><h3>账号：</h3></Col>
                    <Col span="20"><Input v-model="name" /></Col>
                </Row>
                <Row style="margin-top:10px;">
                    <Col span="4"><h3>密码：</h3></Col>
                    <Col span="20"><Input type="password" v-model="password" /></Col>
                </Row>
                <Row style="margin-top:10px;">
                    <Col offset="4" span="20">
                        <Button type="success" long @click='login'>登录</Button>
                    </Col>
                </Row>
            </Col>
        </Row>
    </div>
</template>
<script>
export default {
    data() {
        return {
            name: '',
            password: '',
        }
    },
    methods: {
        login(){
            if (this.name == '') {
                this.$Message.info('请输入用户名')
                return
            }
            if (this.password == '') {
                this.$Message.info('请输入密码')
                return
            }
            const param = {name: this.name, password: this.password}

            this.$axios({
                withCredentials: true,
                method: "POST",
                url:  import.meta.env.VITE_API_BASE_HOST + "/login",
                data: JSON.stringify(param),
                headers:{
                    'Content-Type': "application/json",
                },
            }).then((res)=>{
                console.log(res)
                if(res.status != 200){
                    this.$Message.error('接口异常('+res.status+')')
                    return
                }
                if(res.data.code != 0){
                    this.$Message.error('操作异常('+res.data.message+')')
                    return
                }
                this.$Message.success(res.data.message)
                this.$router.push("/students")
            }).catch((err)=>{
                this.$Message.error('网路异常('+ err + ')')
            })
        }
    },
}

</script>

