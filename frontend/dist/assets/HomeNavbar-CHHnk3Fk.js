import{u as i}from"./index-kI_rcZ0B.js";import{m as c,f as m,ah as f,p as t,q as a,F as p,a7 as u,M as b,O as _,S as d,T as h}from"./vue-DRvwLzXx.js";import{_ as g}from"./index-ClA49R_p.js";const v=c({__name:"HomeNavbar",setup(x){const e=i(),l=e.id;console.log("loginstate.iframeurl123",e.iframeurl),console.log("loginstate:",JSON.stringify(e,null,2));const s=m(()=>[{label:"鲸币申请",href:"/coin/apply"},{label:"鲸币审批",href:"/coin/supervise",visible:l<4},{label:"鲸币消费",href:"/coin/consume"},{label:"鲸币账单",href:"/coin/bill"},{label:"鲸币商品",href:"/item/item"},{label:"鲸币订单",href:"/item/order"},{label:"更新数据",href:"/coin/fetchrepo",visible:l<4}].filter(r=>r.visible!==!1));return(r,k)=>{const n=f("router-link");return t(),a("div",null,[(t(!0),a(p,null,u(s.value,o=>(t(),b(n,{key:o.label,to:o.href,class:"inline-block px-4 py-2 mx-2 my-4 rounded-md bg-custom-color text-white"},{default:_(()=>[d(h(o.label),1)]),_:2},1032,["to"]))),128))])}}}),B=g(v,[["__scopeId","data-v-03876920"]]);export{B as H};
