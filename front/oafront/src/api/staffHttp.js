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

const getStaffList = (page=1,size=10) =>{
    const path = `/staff/staff?page=${page}&size=${size}`
    return http.get(path)
}

export default {    
    getALLDepartment,
    addStaff,
    getStaffList
}