<template>
    <div>
        <Row>
            <Col span="16" offset="4">
                <Row>
                    <Col span="4" style="text-align:left;">
                        <a href="javascript:void(0)" @click='this.$router.push("/students")'>学生成绩管理</a>
                    </Col>
                    <Col span="20" style="text-align:right;">
                        <a href="javascript:void(0)" @click='logout'>退出登录</a>
                    </Col>
                </Row>
                <Row style="text-align:center;display:inline;">
                    <h1>教师账号管理</h1>
                </Row>
                <Row style="margin-top:20px;">
                    <Col span="2" offset="10"><Button type="primary" @click="get_list">查询列表</Button></Col>
                    <Col span="2" offset="1"><Button type="success" @click="show_add">增加账号</Button></Col>
                </Row>
                <Row style="margin-top:20px;">
                    <Col span="24">
                        <Table :columns="columns" :data="data">
                            <template #action="{row, index}">
                                <Button type="info" size="small" @click="show_edit(row)">修改</Button>
                                <Button type="error" size="small" style="margin-left:10px;" @click="del_confirm(row)">删除</Button>
                            </template>
                        </Table>
                    </Col>
                </Row>
            </Col>
        </Row>
    </div>
    <div>
        <Modal
            v-model="add.modal"
            title="新增教师账号信息"
            :loading = "add.loading"
            @on-ok="add_ok"
            @on-cancel="add_cancel">
            <p style="padding:5px;"><Row>
                    <Col span="2">账户</Col>
                    <Col span="22"><Input v-model="add.param.name" size='small' style="width:80%"/></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">密码</Col>
                    <Col span="22"><Input type="password" v-model="add.param.password" size='small' style="width:80%"/></Col>
            </Row></p>
        </Modal>
        <Modal
            v-model="edit.modal"
            title="修改教师账号信息"
            :loading = "edit.loading"
            @on-ok="edit_ok"
            @on-cancel="edit_cancel">
            <p style="padding:5px;"><Row>
                    <Col span="2">教师编码</Col>
                    <Col span="22"><Input v-model="edit.param.id" size='small' style="width:80%" disabled /></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">账户</Col>
                    <Col span="22"><Input v-model="edit.param.name" size='small' style="width:80%"/></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">密码</Col>
                    <Col span="22"><Input type="password" v-model="edit.param.password" size='small' style="width:80%"/></Col>
            </Row></p>
        </Modal>
    </div>
</template>
<script>
export default {
    data() {
        return {
            add:{
                modal: false,
                loading: true,
                param: {
                    name: '',
                    password: '',
                },
            },
            edit:{
                modal: false,
                loading: true,
                param: {
                    id:'',
                    name: '',
                    password: '',
                },
            },
            columns: [
                {
                    title: '教师编码',
                    key: 'id',
                    align: 'center',
                },
                {
                    title: '账户名',
                    key: 'name',
                    align: 'center',
                },
                {
                    title: '操作',
                    slot: 'action',
                    minWidth:120,
                }
            ],
            data: [],
        }
    },
    mounted(){
        this.get_list();
    },
    methods: {
        get_list(){
            this.data = [];
            this.$axios({
                withCredentials: true,
                method: "GET",
                url: import.meta.env.VITE_API_BASE_HOST + "/teacher_list",
            }).then((res)=>{
                if(res.status != 200){
                    this.$Message.error('接口异常('+res.status+')')
                    return
                }
                if(res.data.code == 9999){
                    this.$Message.error(res.data.message)
                    this.$router.push("/login")
                    return
                }
                if(res.data.code != 0){
                    this.$Message.error('操作异常('+res.data.message+')')
                    return
                }
                this.$Message.success(res.data.message)
                this.data = res.data.data
            }).catch((err)=>{
                this.$Message.error('网路异常('+ err + ')')
            })
        },
        show_add(){
            this.add.modal=true;
        },
        add_ok(){
            if(this.add.param.name=='' || this.add.param.password==''){
                this.$Message.error("账户名或密码不能为空")
                this.add.loading = false;
                this.$nextTick(()=>{
                    this.add.loading = true;
                });
                return
            }

            let param = {name: this.add.param.name, password: this.add.param.password}

            this.$axios({
                withCredentials: true,
                method: "POST",
                url: import.meta.env.VITE_API_BASE_HOST + "/teacher_add",
                data: JSON.stringify(param),
                headers:{
                    'Content-Type': "application/json",
                },
            }).then((res)=>{
                if(res.status != 200){
                    this.$Message.error('接口异常('+res.status+')')
                    return
                }
                if(res.data.code == 9999){
                    this.$Message.error(res.data.message)
                    this.$router.push("/login")
                    return
                }
                if(res.data.code != 0){
                    this.$Message.error('操作异常('+res.data.message+')')
                    return
                }
                this.add.modal = false;
                this.add_reset();
                this.$Message.success(res.data.message)
                this.add.loading = false;
                this.$nextTick(()=>{
                    this.add.loading = true;
                });
                this.get_list();
            }).catch((err)=>{
                this.$Message.error('网路异常('+ err + ')')
            })

        },
        add_reset(){
            this.add.param.name='';
            this.add.param.password='';
            this.add.modal = false;
        },
        add_cancel(){
            this.add_reset();
        },
        del_confirm(row){
            const self = this
            this.$Modal.confirm({
                title:"删除确认",
                content: `确认对(${row.name})进行删除操作？`,
                onOk(){
                    self.del_submit(row.id);
                },
                onCancel(){
                    return
                }
            });
        },
        del_submit(id){
           const param = {id:id}
           this.$axios({
                withCredentials: true,
                method: "POST",
                url: import.meta.env.VITE_API_BASE_HOST + "/teacher_del",
                data: JSON.stringify(param),
                headers:{
                    'Content-Type': "application/json",
                },
            }).then((res)=>{
                if(res.status != 200){
                    this.$Message.error('接口异常('+res.status+')');
                    return
                }
                if(res.data.code == 9999){
                    this.$Message.error(res.data.message)
                    this.$router.push("/login")
                    return
                }
                if(res.data.code != 0){
                    this.$Message.error('操作异常('+res.data.message+')');
                    return
                }
                this.$Message.success(res.data.message);
                this.get_list();
            }).catch((err)=>{
                this.$Message.error('网路异常('+ err + ')');
            })
        },
        edit_reset(){
            this.edit.param.id = '';
            this.edit.param.name='';
            this.edit.param.password='';
        },
        show_edit(row){
            this.edit_reset();
            this.edit.param.id = row.id;
            this.edit.param.name = row.name;
            this.edit.modal = true;
        },
        edit_cancel(){
            this.edit_reset();
            this.edit.modal = false;
        },
        edit_ok(){
            if(this.edit.param.name==''){
                this.$Message.error("姓名不能为空")
                this.edit.loading = false;
                this.$nextTick(()=>{
                    this.edit.loading = true;
                });
                return
            }
            let param = {
                id: this.edit.param.id,
                name: this.edit.param.name,
            }
            if(this.edit.param.password != ''){
                param["password"] = this.edit.param.password
            }
            this.$axios({
                withCredentials: true,
                method: "POST",
                url: import.meta.env.VITE_API_BASE_HOST + "/teacher_edit",
                data: JSON.stringify(param),
                headers:{
                    'Content-Type': "application/json",
                },
            }).then((res)=>{
                if(res.status != 200){
                    this.$Message.error('接口异常('+res.status+')')
                    return
                }
                if(res.data.code == 9999){
                    this.$Message.error(res.data.message)
                    this.$router.push("/login")
                    return
                }
                if(res.data.code != 0){
                    this.$Message.error('操作异常('+res.data.message+')')
                    return
                }
                this.edit.modal = false;
                this.edit_reset();
                this.$Message.success(res.data.message)
                this.edit.loading = false;
                this.$nextTick(()=>{
                    this.edit.loading = true;
                });
                this.get_list();
            }).catch((err)=>{
                this.$Message.error('网路异常('+ err + ')')
            })
        },
        logout(){
            this.$axios({
                withCredentials: true,
                method: "POST",
                url: import.meta.env.VITE_API_BASE_HOST + "/logout",
                data: JSON.stringify({}),
                headers:{
                    'Content-Type': "application/json",
                },
            }).then((res)=>{
                if(res.status != 200){
                    this.$Message.error('接口异常('+res.status+')')
                    return
                }
                if(res.data.code == 9999){
                    this.$Message.error(res.data.message)
                    this.$router.push("/login")
                    return
                }
                if(res.data.code != 0){
                    this.$Message.error('操作异常('+res.data.message+')')
                    return
                }
                this.$Message.success(res.data.message)
                this.$router.push("/login")
            }).catch((err)=>{
                this.$Message.error('网路异常('+ err + ')')
            })
        },
    },
}
</script>