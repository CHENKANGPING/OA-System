import http from './http';

const getALLDepartment = () =>{
    const path = "/staff/departments"
    return http.get(path)
}

export default {
    getALLDepartment,
}