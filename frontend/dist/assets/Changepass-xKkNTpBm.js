import{C as h}from"./api-D12zC24N.js";import{u as b}from"./index-DW3BOA4A.js";import{m as k,a as C,Z as d,ah as l,p as V,q as v,U as a,O as n,S as y,F as x}from"./vue-DRvwLzXx.js";import"./base-CSL5GuM5.js";const i="70px",E=k({__name:"Changepass",setup(P){document.title="修改密码";const u=b(),p=C(),o=d({password:"",checkpass:""}),c=d({password:[{required:!0,message:"请输入密码",trigger:"blur"},{min:6,message:"密码应不少于六位",trigger:"blur"}],checkpass:[{validator:(s,e,t)=>{e===""?t(new Error("请再次输入密码")):e!==o.password?(console.log("密码不一致"),console.log(s),t(new Error("密码不一致!"))):t()},trigger:"blur"}]}),f=async s=>{s&&await s.validate(e=>{e?(console.log(o),_()):alert("请完善密码!")})},_=async()=>{let s={name:u.name,newpass:o.password};(await h(s)).code==200?(alert("修改密码成功！"),o.password="",o.checkpass=""):alert("修改密码失败！")};return(s,e)=>{const t=l("el-input"),m=l("el-form-item"),g=l("el-form"),w=l("el-button");return V(),v(x,null,[a(g,{model:o,ref_key:"ruleFormRef",ref:p,rules:c,"status-icon":""},{default:n(()=>[a(m,{label:"新密码",prop:"password","label-width":i},{default:n(()=>[a(t,{modelValue:o.password,"onUpdate:modelValue":e[0]||(e[0]=r=>o.password=r),type:"password",autocomplete:"off"},null,8,["modelValue"])]),_:1}),a(m,{label:"确认密码",prop:"checkpass","label-width":i},{default:n(()=>[a(t,{modelValue:o.checkpass,"onUpdate:modelValue":e[1]||(e[1]=r=>o.checkpass=r),type:"password",autocomplete:"off"},null,8,["modelValue"])]),_:1})]),_:1},8,["model","rules"]),a(w,{type:"primary",onClick:e[2]||(e[2]=r=>f(p.value))},{default:n(()=>[y("确认")]),_:1})],64)}}});export{E as default};
