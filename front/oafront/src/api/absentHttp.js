import http from "@/api/http.js";

const getAbsentTypes = () =>{
    const path = "/absent/type"
    return http.get(path)
}


const getResponder = () =>{
    const path = "/absent/responder"
    return http.get(path)
}

const applyAbsent = (data) =>{
    const path = "/absent/absent"
    return http.post(path,data)
}

const  getMyAbsents = (page=1) =>{
    const path = "/absent/absent?who=my&page="+page
    return http.get(path)

}


export default {
    getAbsentTypes,
    getResponder,
    applyAbsent,
    getMyAbsents
}