((function(){var a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v;f=function(a){return a.val().length>0};v=function(a){return a.val().length===5};j=function(a){return a.val().length>0};t=function(a){return a.val()>0};o=function(a){if(a.attr("checked")!=="checked")return!0;if(!f($("#mailing_address")))return!1;if(!t($("#mailing_state")))return!1;if(!j($("#mailing_city")))return!1;if(!v($("#mailing_zip_code")))return!1};s=function(a){if(a.attr("checked")!=="checked")return!0;if(!f($("#prev_address")))return!1;if(!t($("#prev_state")))return!1;if(!j($("#prev_city")))return!1;if(!v($("#prev_zip_code")))return!1};u=function(a){return a.val().length>0};l=function(a){return a.val().length>0};n=function(a){return a.val().length>0};h=function(a){if(a.attr("checked")!=="checked")return!0;if(!u($("#prev_name_title")))return!1;if(!l($("#prev_first_name")))return!1;if(!n($("#prev_last_name")))return!1};m=function(a){var b,c,d;c=a.attr("data-maxlength");d=a.attr("data-minlength");b=a.val().length;return d>b||b>c?!1:!0};g=function(a){var b,c,d,e;e=new Date;c=new Date(a.val());b=e.getFullYear()-c.getFullYear();d=e.getMonth()-c.getMonth();(d<0||d===0&&e.getDate()<c.getDate())&&b--;return b<18?!1:!0};k=function(a){var b;b=/^(([^<>()\[\]\\.,;:\s@\"]+(\.[^<>()\[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;return b.test(a.val())};q=function(a){var b;b=/(1-)?[(]*(\d{3})[) -.]*(\d{3})[ -.]*(\d{4})\D*/;return b.test(a.val())};r=function(a){var b;b=a.attr("data-required");return b===!0&&(a.val().length=0)?!1:!0};p=function(a){var b;b=a.attr("data-required");return b===!0&&(a.val().length=0)?!1:!0};i=function(a){return a.attr("checked")!=="checked"?!1:!0};d=function(){var a,b,c,d;b=$("#pre_first_name").val();c=$("#pre_last_name").val();a=$("#pre_email_address").val();d=$("#pre_zip_code");$("#first_name").val(b);$("#last_name").val(c);$("#email_address").val(a);$("#home_zip_code").val(d);$("#state_form").hide();return $("#registration_form").show()};a=function(a){return $.ajax({type:"get",url:"/usps/zip_lookup/",data:{zip:a},success:function(a){$("form#ovr #home_zip_code").val(a.zip);$("form#ovr #home_city").val(a.city);$("form#ovr #home_state_id").val(a.state);return b()},error:function(a){}})};b=function(){var a,b;b="/api/v1/state_requirements.json";a={};a["'home_zip_code'"]=$("#pre_zip_code").val();a["'lang'"]=$("#lang_id").val();return $.ajax({url:b,data:a,type:"get",success:function(a){var b,c,e,f,g,h,i,j,k;if(a.party_list){h=a.party_list;b=$("select#party");c="";for(j=0,k=h.length;j<k;j++){e=h[j];i=h[e];c+="<option val="+i+">"+i+"</option>\n"}a.no_party_msg==="Decline to state"&&(c+='<option val="Decline to state">Decline to state</option>\n');b.append(c)}a.requires_party&&$("#party").attr("data-required",!0);a.requires_party&&$("#party").attr("data-required",!0);a.id_number_msg&&$("#tooltip_text_id_number").text(a.id_number_msg);a.requires_party_msg&&$("#tooltip_text_party").text(a.requires_party_msg);a.requires_race_msg&&$("#tooltip_text_race").text(a.requires_race_msg);g=a.id_min_length||0;f=a.id_max_length||100;$("#id_number").attr("data-maxlength",f).attr("data-minlength",g);return d()},error:function(a){}})};e=function(){return a($("#pre_zip_code").val())};c=function(){$("#registration_form").hide();$(".mailing").hide();$(".name-change").hide();$(".address-change").hide();return $("form#get_started").submit(function(a){a.preventDefault();return e()})};jQuery(function(a){return c()})})).call(this);