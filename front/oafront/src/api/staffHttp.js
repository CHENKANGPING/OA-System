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



export default {    
    getALLDepartment,
    addStaff
}