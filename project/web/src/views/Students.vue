<template>
    <div>
        <Row>
            <Col span="16" offset="4">
                <Row>
                    <Col span="4" style="text-align:left;">
                        <a href="javascript:void(0)" @click='this.$router.push("/teachers")'>教师账号管理</a>
                    </Col>
                    <Col span="20" style="text-align:right;">
                        <a href="javascript:void(0)" @click='logout'>退出登录</a>
                    </Col>
                </Row>
                <Row style="text-align:center;display:inline;">
                    <h1>学生成绩管理</h1>
                </Row>
                <Row style="margin-top:20px;">
                    <Col span="2" offset="10"><Button type="primary" @click="get_students">查询列表</Button></Col>
                    <Col span="2" offset="1"><Button type="success" @click="show_add">增加</Button></Col>
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
            title="新增学生信息"
            :loading = "add.loading"
            @on-ok="add_ok"
            @on-cancel="add_cancel">
            <p style="padding:5px;"><Row>
                    <Col span="2">姓名</Col>
                    <Col span="22"><Input v-model="add.param.name" size='small' style="width:80%"/></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">英语</Col>
                    <Col span="22"><Input v-model="add.param.english" size='small' style="width:80%"/></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">语文</Col>
                    <Col span="22"><Input v-model="add.param.chinese" size='small' style="width:80%"/></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">数学</Col>
                    <Col span="22"><Input v-model="add.param.math" size='small' style="width:80%"/></Col>
            </Row></p>
        </Modal>
        <Modal
            v-model="edit.modal"
            title="修改学生信息"
            :loading = "edit.loading"
            @on-ok="edit_ok"
            @on-cancel="edit_cancel">
            <p style="padding:5px;"><Row>
                    <Col span="2">学号</Col>
                    <Col span="22"><Input v-model="edit.param.id" size='small' style="width:80%" disabled /></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">姓名</Col>
                    <Col span="22"><Input v-model="edit.param.name" size='small' style="width:80%"/></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">英语</Col>
                    <Col span="22"><Input v-model="edit.param.english" size='small' style="width:80%"/></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">语文</Col>
                    <Col span="22"><Input v-model="edit.param.chinese" size='small' style="width:80%"/></Col>
            </Row></p>
            <p style="padding:5px;"><Row>
                    <Col span="2">数学</Col>
                    <Col span="22"><Input v-model="edit.param.math" size='small' style="width:80%"/></Col>
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
                    english: '',
                    chinese: '',
                    math: '',
                },
            },
            edit:{
                modal: false,
                loading: true,
                param: {
                    id:'',
                    name: '',
                    english: '',
                    chinese: '',
                    math: '',
                },
            },
            columns: [
                {
                    title: '学号',
                    key: 'id',
                    align: 'center',
                },
                {
                    title: '姓名',
                    key: 'name',
                    align: 'center',
                },
                {
                    title: '英语',
                    key: 'english',
                    align: 'center',
                },
                {
                    title: '语文',
                    key: 'chinese',
                    align: 'center',
                },
                {
                    title: '数学',
                    key: 'math',
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
        this.get_students();
    },
    methods: {
        get_students(){
            this.data = [];
            this.$axios({
                withCredentials: true,
                method: "GET",
                url: import.meta.env.VITE_API_BASE_HOST + "/student_list",
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
            if(this.add.param.name==''){
                this.$Message.error("姓名不能为空")
                this.add.loading = false;
                this.$nextTick(()=>{
                    this.add.loading = true;
                });
                return
            }

            let param = {name: this.add.param.name}
            if(this.add.param.english != ''){
                param.english = this.add.param.english
            }
            if(this.add.param.chinese != ''){
                param.chinese = this.add.param.chinese
            }
            if(this.add.param.math != ''){
                param.math = this.add.param.math
            }
            this.$axios({
                withCredentials: true,
                method: "POST",
                url: import.meta.env.VITE_API_BASE_HOST + "/student_add",
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
                this.get_students();
            }).catch((err)=>{
                this.$Message.error('网路异常('+ err + ')')
            })

        },
        add_reset(){
            this.add.param.name='';
            this.add.param.english='';
            this.add.param.chinese='';
            this.add.param.math='';
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
                url: import.meta.env.VITE_API_BASE_HOST + "/student_del",
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
                this.get_students();
            }).catch((err)=>{
                this.$Message.error('网路异常('+ err + ')');
            })
        },
        edit_reset(){
            this.edit.param.id = '';
            this.edit.param.name='';
            this.edit.param.english='';
            this.edit.param.chinese='';
            this.edit.param.math='';
        },
        show_edit(row){
            this.edit_reset();
            this.edit.param.id = row.id;
            this.edit.param.name = row.name;
            this.edit.param.english = row.english;
            this.edit.param.chinese = row.chinese;
            this.edit.param.math = row.math;
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
            const param = {
                id: this.edit.param.id,
                name: this.edit.param.name,
                english: this.edit.param.english,
                chinese: this.edit.param.chinese,
                math: this.edit.param.math,
            }
            this.$axios({
                withCredentials: true,
                method: "POST",
                url: "http://localhost:9000/student_edit",
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
                this.get_students();
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