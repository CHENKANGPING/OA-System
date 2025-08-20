import http from "@/api/http.js";

const getDepartmentStaffCount = () => {
    const path = "/home/department/staff/count"
    return http.get(path)
}

const getLatestInforms = () => {
    const path = "/home/latest/inform"
    return http.get(path)
}

const getLatestAbsents = () => {
    const path = "/home/latest/absent"
    return http.get(path)
}

export default {
    getDepartmentStaffCount,  
    getLatestInforms,         
    getLatestAbsents
}