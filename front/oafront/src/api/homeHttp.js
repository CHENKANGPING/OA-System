import http from "@/api/http.js";

const getDepartmentStaffCont = () => {
    const path = "/home/department/staff/count"
    return http.get(path)
}

const getLatestInform = () => {
    const path = "/home/latest/inform"
    return http.get(path)
}


const getLatestAbsents = () => {
    const path = "/home/latest/absent"
    return http.get(path)
}


export default {
    getDepartmentStaffCont,
    getLatestInform,
    getLatestAbsents

}