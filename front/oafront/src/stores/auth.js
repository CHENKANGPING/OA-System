import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

const USER_KEY = "OA_USER_KEY";
const TOKEN_KEY = "OA_TOKEN_KEY";

export const PermissionChoices = {
  // 所有权限
  All: 0b111,
  // 普通员工权限
  Staff: 0b000,
  // 需要董事会权限
  Boarder: 0b001,
  // TeamLeader权限
  Leader: 0b010,
}

export const useAuthStore = defineStore('auth', () => {
    let _user = ref({});
    let _token = ref(''); // 修改：初始化为空字符串而不是空对象

    function setUerToken(user, token) {
        // 保存到对象上(内存中)
        _user.value = user;
        _token.value = token;

        // 存储到浏览器的localStorge(硬盘上)
        localStorage.setItem(USER_KEY, JSON.stringify(user));
        localStorage.setItem(TOKEN_KEY, token);
    }

    function clearUerToken(){
        _user.value = {};
        _token.value = ''; // 修改：清空为空字符串
        localStorage.removeItem(USER_KEY);
        localStorage.removeItem(TOKEN_KEY);
    }

    // 计算属性
    let user = computed(() => {
        // 如果_user是一个空对象，那么就视图从localStorge中获取
        if (Object.keys(_user.value).length == 0) {
            let user_str = localStorage.getItem(USER_KEY);
            if (user_str) {
                _user.value = JSON.parse(user_str);
            }
        }
        return _user.value;
    });
    
    // 计算属性
    let token = computed(() => {
        // 修改：正确判断空字符串
        if (!_token.value || _token.value === '') {
            let token_str = localStorage.getItem(TOKEN_KEY);
           if(token_str){
            _token.value = token_str;
           }
        }
        return _token.value;
    });

    let  is_logined = computed(() =>{
      if(Object.keys(user.value).length>0 && token.value){
        return true;
      }
      return false;
    })

    let own_permissions = computed(() => {
    // 0b000
    let _permissions = PermissionChoices.Staff
    if(is_logined.value){
      // 判断是否是董事会成员
      if(user.value.department.name == '董事会'){
        // 0b000 | 0b001 = 0b001
        _permissions |= PermissionChoices.Boarder
      }

      // 判断是否是team leader
      if(user.value.department.leader_id == user.value.uid){
        _permissions |= PermissionChoices.Leader
      }
    }
    return _permissions
  })

  function has_permission(permissions, opt='|'){
    // opt可选值：
    // 1. |：或运算
    // 2. &：且运算
    // own_permissions: 0b001
    // permissions: [0b010, 0b001]
    let results = permissions.map((permission) => (permission&own_permissions.value)==permission)
    // results = [true, false, false, true]
    if(opt == "|"){
      if(results.indexOf(true) >= 0){
        return true;
      }else{
        return false;
      }
    }else{
      if(results.indexOf(false) >= 0){
        return false;
      }else{
        return true
      }
    }
  }

    // 想要让外面访问，就必须要返回
    return { setUerToken, user, token,is_logined ,clearUerToken,has_permission}
})