import http from './http';

const getALLDepartment = () =>{
    const path = "/staff/departments"
    return http.get(path)
}

const addStaff = (realname,email,password) =>{
    const path = "/staff/staff"
    return http.post(path,{
        realname,
        email,
        password,
    })
}

const getStaffList = (page=1,size=10,params) =>{
    const path = `/staff/staff`
    params = params?params:{}
    params['page'] = page
    params['size'] = size

    return http.get(path,params)
}

const updateStaffStatus =(staff_id,status) =>{
    const path  = "/staff/staff/" + staff_id
    return http.put(path,{
        status
    })
}

const dowoloadStaffs = (pks) =>{
    const path = "/staff/download"
    // 关键修改：不要手动 encodeURIComponent，也不要自己拼接 URL
    // 直接把 JSON 字符串作为 params 传入，让 axios 负责序列化
    return http.downloadFile(path, { pks: JSON.stringify(pks) })
}


export default {    
    getALLDepartment,
    addStaff,
    getStaffList,
    updateStaffStatus,
    dowoloadStaffs
}