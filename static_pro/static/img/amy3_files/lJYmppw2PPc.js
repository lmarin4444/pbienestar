if (self.CavalryLogger) { CavalryLogger.start_js(["\/mnVq"]); }

__d("PhotoTagApproval",["Arbiter","CSS","DOM","Event","Parent","PhotosConst","ge"],(function a(b,c,d,e,f,g){function h(i){"use strict";this.viewer=i;this.units=[];this.currentUnit=0;var j=i.getVersionConst();if(j==c("PhotosConst").VIEWER_SNOWLIFT)this._root=c("ge")("fbPhotoSnowliftTagApproval");else this._root=c("ge")("fbPhotoPageTagApproval");c("Arbiter").subscribe(i.getEventString("DATA_CHANGE"),this.restartTagApproval.bind(this));c("Arbiter").subscribe("PhotoTagApproval.PENDING_TAG_PHOTO_CLICK",this.pendingTagPhotoClick.bind(this));c("Event").listen(this._root,"click",this.handleClick.bind(this));c("Event").listen(this._root,"mousemove",function(k){this.hiliteCurrentPendingTag();c("Event").kill(k)}.bind(this));this.restartTagApproval()}h.prototype.handleClick=function(event){"use strict";var i=event.getTarget();if(c("CSS").hasClass(i,"nextPager")&&c("CSS").hasClass(i,"enabled"))this.showNextUnit();else if(c("CSS").hasClass(i,"prevPager")&&c("CSS").hasClass(i,"enabled"))this.showPrevUnit();else if(c("Parent").byClass(i,"fbPhotoApprovalPendingButtons")){var j=this.units[this.currentUnit],k=this.getTagNameID(j);if(k){var l=c("Parent").byClass(i,"approve");c("Arbiter").inform("PhotoTagApproval.UPDATE_TAG_BOX",{id:k,approve:l,version:this.viewer.getVersionConst()})}setTimeout(this.removeSelectedUnit.bind(this),0)}return true};h.prototype.loadUnits=function(i){"use strict";this.units=c("DOM").scry(this._root,"div.fbPhotoApprovalUnit");if(this.units.length){c("CSS").show(this._root);this.showUnit(i);c("CSS").conditionClass(this._root,"hidePagers",this.units.length==1)}else{c("CSS").hide(this._root);c("Arbiter").inform("PhotoTagApproval.HILITE_TAG",{tag:null,version:this.viewer.getVersionConst()})}};h.prototype.restartTagApproval=function(){"use strict";this.loadUnits(0)};h.prototype.pendingTagPhotoClick=function(i,j){"use strict";if(j.version!==c("PhotosConst").VIEWER_PERMALINK&&j.version!==c("PhotosConst").VIEWER_SNOWLIFT)return true;var k="approve:"+j.id;for(var l=0;l<this.units.length;l++)if(this.units[l].id===k){this.showUnit(l);return false}return true};h.prototype.removeSelectedUnit=function(){"use strict";var i=this.units[this.currentUnit];c("DOM").remove(i);this.loadUnits(this.currentUnit)};h.prototype.showNextUnit=function(){"use strict";this.showUnit(this.currentUnit+1)};h.prototype.showPrevUnit=function(){"use strict";this.showUnit(this.currentUnit-1)};h.prototype.getTagNameID=function(i){"use strict";var j=i.id.indexOf(":");return i.id.slice(j+1)};h.prototype.showUnit=function(i){"use strict";this.units.forEach(c("CSS").hide);this.currentUnit=(i+this.units.length)%this.units.length;var j=this.units[this.currentUnit];c("CSS").show(j);this.hiliteCurrentPendingTag();c("CSS").conditionClass(c("DOM").find(this._root,"a.prevPager"),"enabled",this.currentUnit>0);c("CSS").conditionClass(c("DOM").find(this._root,"a.nextPager"),"enabled",this.currentUnit<this.units.length-1)};h.prototype.hiliteCurrentPendingTag=function(){"use strict";var i=this.units[this.currentUnit],j=this.getTagNameID(i);c("Arbiter").inform("PhotoTagApproval.HILITE_TAG",{tag:j,version:this.viewer.getVersionConst()})};f.exports=h}),null);
__d("PhotoTags",["csx","Arbiter","CSS","DOM","Event","Parent","PhotosConst","ge"],(function a(b,c,d,e,f,g,h){function i(j,k,l){"use strict";this.tagTargets=j;this.tagBox=k;this.version=l||c("PhotosConst").VIEWER_PERMALINK;this.handlers=[];this.tagTargets.forEach(function(m){this.handlers.push(c("Event").listen(m,{mouseover:this.showTag.bind(this),mouseout:this.hideTags.bind(this)}))}.bind(this));this.subscriptions=[];if(this.version==c("PhotosConst").VIEWER_SNOWLIFT)this.subscriptions.push(c("Arbiter").subscribe("PhotoSnowlift.PAGE",this.hideTags.bind(this)))}i.prototype.showTag=function(event){"use strict";var j=event.getTarget(),k=c("CSS").hasClass(j,"taggee"),l=c("CSS").matchesSelector(j,"._54ru"),m=null,n=null;if(k){m=j.getAttribute("data-tag");n=j.getAttribute("data-tagtype")}else if(l){var o=c("Parent").byTag(j,"a");m=o&&o.getAttribute("data-tag")}if(!m){j=c("Parent").byClass(j,"taggee");if(j){m=j.getAttribute("data-tag");n=j.getAttribute("data-tagtype")}}var p=this.version==c("PhotosConst").VIEWER_PERMALINK?"perm:tag:"+m:"tag:"+m,q=p&&c("ge")(p);if(q){if(n==="product")c("CSS").addClass(q,"hover");else c("CSS").addClass(q,"showTag");c("CSS").addClass(this.tagBox,"showingTag");c("Arbiter").inform("PhotoTags.SHOWTAG",m)}};i.prototype.hideTags=function(){"use strict";c("CSS").removeClass(this.tagBox,"showingTag");c("DOM").scry(this.tagBox,"div.showTag").forEach(function(j){c("CSS").removeClass(j,"showTag")});c("DOM").scry(this.tagBox,"div.hover").forEach(function(j){c("CSS").removeClass(j,"hover")});c("Arbiter").inform("PhotoTags.HIDETAG")};i.prototype.destroy=function(){"use strict";for(var j in this.handlers)this.handlers[j].remove();this.subscriptions.forEach(c("Arbiter").unsubscribe,c("Arbiter"))};f.exports=i}),null);
__d("PhotoViewerFollow",["Arbiter","AsyncRequest","BanzaiODS","CSS","DOM","Event","Parent","PhotosConst","$","collectDataAttributes"],(function a(b,c,d,e,f,g){var h={};function i(j){"use strict";this.FOLLOW_LOCATION_PHOTO=48;this.viewer=j}i.prototype.init=function(j,k,l,m,n,o,p){"use strict";this.subscribeLink=j;this.unsubscribeFlyout=k;this.subscribeEndpoints=n;this.unsubscribeEndpoints=o;this.unsubLinks=m;this.unsubDiv=l;this.reset();this.activate();this.type=p;c("Event").listen(this.subscribeLink,"click",function(event){if(c("Parent").byClass(event.getTarget(),"photoViewerFollowLink"))this.subscribePhotoOwner()}.bind(this));c("Event").listen(this.unsubLinks.user,"click",this.unsubscribePhotoOwner.bind(this));c("Event").listen(this.unsubLinks.page,"click",this.unsubscribePhotoOwner.bind(this));c("Arbiter").subscribe(["FollowUser","FollowUserFail","UnfollowUser","UnfollowUserFail"],this.updateSubscribe.bind(this));c("Arbiter").subscribe(this.viewer.getEventString("DATA_CHANGE"),this.showSubscribeLinkOnChange.bind(this));if(this.viewer.getVersionConst()===c("PhotosConst").VIEWER_SNOWLIFT){c("Arbiter").subscribe(this.viewer.getEventString("CLOSE"),this.reset.bind(this));c("Arbiter").subscribe(this.viewer.getEventString("OPEN"),this.activate.bind(this))}this.registerUnsubscribeTarget()};i.prototype.activate=function(){"use strict";this.activated=true};i.prototype.reset=function(){"use strict";this.unsubscribeFlyout&&this.unsubscribeFlyout.clearNodes();this.subscriptionChange={};this.activated=false};i.prototype.registerUnsubscribeTarget=function(){"use strict";if(!this.unsubscribeFlyout)return;var j=c("DOM").scry(this.subscribeLink,".photoViewerFollowedMsg")[0];if(j&&!c("CSS").hasClass(j,"unsubFlyoutEnabled")){this.unsubscribeFlyout.initNode(j);c("CSS").addClass(j,"unsubFlyoutEnabled")}};i.prototype.updateSubscribe=function(j,k){"use strict";if(!this.activated)return;var l=k.profile_id;if(l){this.subscriptionChange[l]=j==="FollowUser"||j==="UnfollowUserFail"?"following":"unfollowed";this.toggleSubscribeLink(l)}};i.prototype.showSubscribeLinkOnChange=function(j,k){"use strict";this.type=k.ownertype;c("CSS").conditionClass(this.unsubDiv,"isPage",this.type==="page");this.toggleSubscribeLink(k.owner)};i.prototype.toggleSubscribeLink=function(j){"use strict";var k=c("DOM").scry(this.subscribeLink,"span.fbPhotoSubscribeWrapper")[0];if(!k)return;if(this.subscriptionChange[j]){c("CSS").conditionClass(k,"followingOwner",this.subscriptionChange[j]==="following");if(this.subscriptionChange[j]==="unfollowed")this.unsubscribeFlyout&&this.unsubscribeFlyout.hideFlyout(true)}this.registerUnsubscribeTarget()};i.prototype.subscribePhotoOwner=function(){"use strict";if(!this.viewer.getOwnerId())return;var j=this.type==="user"?{profile_id:this.viewer.getOwnerId()}:{fbpage_id:this.viewer.getOwnerId(),add:true,reload:false,fan_origin:"photo_snowlift"};c("Arbiter").inform("FollowUser",{profile_id:this.viewer.getOwnerId()});if(this.type==="page")c("BanzaiODS").bumpEntityKey("snowlift_page_like","snowlift_page_like.clicked_link");j.location=this.FOLLOW_LOCATION_PHOTO;var k=event.getTarget();if(k)Object.assign(j,{ft:c("collectDataAttributes")(k,["ft"]).ft});new(c("AsyncRequest"))(this.subscribeEndpoints[this.type]).setAllowCrossPageTransition(true).setData(j).setMethod("POST").setReadOnly(false).setErrorHandler(c("Arbiter").inform.bind(null,"FollowUserFail",j)).send()};i.prototype.unsubscribePhotoOwner=function(){"use strict";if(!this.viewer.getOwnerId())return;var j=this.type==="user"?{profile_id:this.viewer.getOwnerId()}:{fbpage_id:this.viewer.getOwnerId(),add:false,reload:false};c("Arbiter").inform("UnfollowUser",{profile_id:this.viewer.getOwnerId()});j.location=this.FOLLOW_LOCATION_PHOTO;var k=event.getTarget();if(k)Object.assign(j,{ft:c("collectDataAttributes")(k,["ft"]).ft});new(c("AsyncRequest"))(this.unsubscribeEndpoints[this.type]).setAllowCrossPageTransition(true).setData(j).setMethod("POST").setReadOnly(false).setErrorHandler(c("Arbiter").inform.bind(null,"UnfollowUserFail",j)).send()};i.createInstance=function(j,k,l,m,n,o,p,q){"use strict";var r=j.getInstance(),s=new i(r);s.init(c("$")(k),l,m,n,o,p,q);h[r.getVersionConst()]=s;return s};i.getInstance=function(j){"use strict";return h[j]};f.exports=i}),null);
__d("PhotoViewerInitPagelet",["DOM","PhotoSnowlift","PhotoTagApproval","PhotoTagger","PhotoTags","ge"],(function a(b,c,d,e,f,g){function h(i){"use strict";c("PhotoSnowlift").attachTagger(i.tagging,i.tokenizer,i.ufi);var j=c("PhotoSnowlift").getInstance(),k=j.getRoot();new(c("PhotoTags"))([c("ge")("fbPhotoSnowliftAuthorName"),c("DOM").find(k,"span.fbPhotoTagList"),c("DOM").find(k,"div.fbPhotoProductsTagList")],c("ge")("fbPhotoSnowliftTagBoxes"),i.version);if(i.setupPhotoTagger){var l=new(c("PhotoTagger"))(j);l.initSnowlift(i.tagging,i.tokenizer,i.userId,i.ufi);l.setQueueName(i.queueName)}new(c("PhotoTagApproval"))(j)}f.exports=h}),null);
__d("TagToken",["DOM","Token"],(function a(b,c,d,e,f,g){var h,i;h=babelHelpers.inherits(j,c("Token"));i=h&&h.prototype;function j(k){"use strict";i.constructor.call(this,k,"tag")}j.prototype.createElement=function(){"use strict";var k=this.isFreeform(),l=c("DOM").create("span",{className:"separator"},", "),m=c("DOM").create(k?"span":"a",{className:"taggee","data-tag":this.getValue()},this.getText());if(!k)m.href=this.getInfo().path;return c("DOM").create("span",{className:"tagItem"},[l,m])};f.exports=j}),null);
__d("TagTokenizer",["fbt","Arbiter","CSS","DOM","Parent","TagToken","Tokenizer","createObjectFrom","ge","getElementText"],(function a(b,c,d,e,f,g,h){var i,j;i=babelHelpers.inherits(k,c("Tokenizer"));j=i&&i.prototype;function k(l,m,n,o,p){"use strict";j.constructor.call(this,n,o,p);c("Arbiter").subscribe("PhotoInlineEditor.CANCEL_INLINE_EDITING",this.updateTokenareaVisibility.bind(this),c("Arbiter").SUBSCRIBE_NEW);this.appphoto=m;c("Arbiter").subscribe(l.getInstance().getEventString("DATA_CHANGE"),this.setup.bind(this),c("Arbiter").SUBSCRIBE_NEW)}k.prototype.setup=function(l,m){"use strict";this.appphoto=m.byapp;this.byowner=m.isowner;return this.reset()};k.prototype.reset=function(){"use strict";var l=this.getTokenElements().map(this.getTokenDataFromTag,this);this.withTagKeys={};var m=this.getWithTagTokenElements().map(function(n){return this._tokenKey(this.getTokenDataFromTag(n))}.bind(this));this.withTagKeys=c("createObjectFrom")(m);return j.reset.call(this,l)};k.prototype.processEvents=function(event,l,m){"use strict";if(c("Parent").byClass(l,"remove")){var n=this.getTokenFromElement(m);n=this.addTokenData(n,l);this.removeToken(n);event.kill()}};k.prototype.insertToken=function(l){"use strict";return null};k.prototype.removeToken=function(l){"use strict";if(this.appphoto)return this.replaceToken(l);else{this.inform("removeToken",l);c("Arbiter").inform("Form/change",{node:this.element})}return null};k.prototype.addTokenData=function(l,m){"use strict";if(c("Parent").byClass(m,"blockuser"))l.blockUser=true;return l};k.prototype.getTokenDataFromTag=function(l){"use strict";return{uid:c("DOM").find(l,"input").value,text:c("getElementText")(c("DOM").find(l,".taggee"))}};k.prototype.getTokenElementFromTarget=function(l){"use strict";return c("Parent").byClass(l,"tagItem")};k.prototype.getTokenElements=function(){"use strict";return c("DOM").scry(this.tokenarea,"span.tagItem").filter(this.filterNonTokenElements,this)};k.prototype.getWithTagTokenElements=function(){"use strict";return c("DOM").scry(this.tokenarea,"span.withTagItem")};k.prototype.filterNonTokenElements=function(l){"use strict";return!c("CSS").hasClass(l,"markasspam")&&!c("CSS").hasClass(l,"reported")&&!c("CSS").hasClass(l,"withTagItem")};k.prototype.createToken=function(l,m){"use strict";var n=this.getToken(this._tokenKey(l));n=n||new(c("TagToken"))(l);m&&n.setElement(m);return n};k.prototype.updateTokenareaVisibility=function(){"use strict";var l=this.getTokenElements().filter(function(o){return c("CSS").shown(o)}),m=this.getWithTagTokenElements(),n=c("DOM").scry(this.tokenarea,"span.ogTagItem");c("CSS").conditionShow(this.tokenarea,l.length!==0||m.length!==0||n.length!==0)};k.prototype.replaceToken=function(l){"use strict";if(!l)return;var m=this.tokens.indexOf(l);if(m<0)return;this.tokens.splice(this.tokens.indexOf(l),1);delete this.unique[this._tokenKey(l.getInfo())];var n=c("ge")("tagspam"+l.getValue());n&&c("DOM").remove(n);var o=[" [",h._("Etiqueta eliminada.")," "];o.push(c("DOM").create("a",{onclick:this.markAsSpam.bind(this,l.getValue())},h._("Marcar etiqueta como ofensiva")));o.push("] ");var p=c("DOM").create("span",{className:"fbPhotosTaglistTag tagItem markasspam",id:"tagspam"+l.getValue()},o);c("DOM").replace(l.getElement(),p);this.updateTokenarea();this.inform("removeToken",l);c("Arbiter").inform("Form/change",{node:this.element})};k.prototype.markAsSpam=function(l){"use strict";var m=c("ge")("tagspam"+l),n=[" [",h._("Etiqueta Reportada"),"] "],o=c("DOM").create("span",{className:"fbPhotosTaglistTag tagItem reported",id:"tagspam"+l},n);c("DOM").replace(m,o);this.inform("markTagAsSpam",l)};k.prototype.removeTokenForSpatialTag=function(l){"use strict";j.removeToken.call(this,l)};f.exports=k}),null);