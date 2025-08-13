<script setup name="staffadd">
import { ref, reactive } from 'vue';
import staffHttp from '@/api/staffHttp';
import { useRouter } from 'vue-router';
import OAMain from "@/components/OAMain.vue"
import {useAuthStore} from "@/stores/auth"
import { ElMessage } from 'element-plus';


const router = useRouter();
const authStore = useAuthStore()

// 只有部门的leader可以给本部门新增员工
let staffForm = reactive({
    email: "",
    password: "",
    realname: "",
});
const formRef = ref()
let rules = reactive({
    email: [{required: true, message: "请输入邮箱！", trigger: 'blur'}],
    password: [{required: true, message: "请输入密码！", trigger: 'blur'}],
    realname: [{required: true, message: "请输入真实姓名！", trigger: 'blur'}],
})

const onSubmit = () => {
    formRef.value.validate(async(valid,fields) => {
        if(valid){
            try{
                await staffHttp.addStaff(staffForm.realname,staffForm.email,staffForm.password)
                ElMessage.success('员工添加成功！')
                router.push({name: 'staff_list'})
            }catch(detial){
                ElMessage.error(detial)
            }
        }
    })
}

</script>

<template>
    <OAMain title="新增员工">
        <el-card shadow="always">
            <el-form :rules="rules" :model="staffForm" ref="formRef" label-width="80px">
                <el-form-item label="姓名" prop="realname">
                    <el-input v-model="staffForm.realname" placeholder="请输入姓名">
                    </el-input>
                </el-form-item>

                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="staffForm.email" placeholder="请输入邮箱"> </el-input>
                </el-form-item>

                <el-form-item label="密码" prop="password">
                    <el-input v-model="staffForm.password" placeholder="请输入密码" type="password">
                    </el-input>
                </el-form-item>

                <el-form-item label="部门">
                    <el-input readonly disabled placeholder="请输入部门" :value="authStore.user.department.name">
                    </el-input>
                </el-form-item>

                <el-form-item label="领导">
                    <el-input readonly disabled :placeholder="'[' + authStore.user.email + ']' + authStore.user.realname">
                    </el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="onSubmit"> 提交 </el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </OAMain>
</template>

<style scoped></style>