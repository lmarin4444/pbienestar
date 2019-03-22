if (self.CavalryLogger) { CavalryLogger.start_js(["6FpxG"]); }

__d("BoostedComponentMainDialogV2ContainerWrapper.react",["BoostedActionMainDialogV2Container.react","BoostedComponentAppIDUtils","BoostedComponentDialogUIActionsV2","BoostedPostMainDialogV2Container.react","React"],(function a(b,c,d,e,f,g){"use strict";var h,i;h=babelHelpers.inherits(j,c("React").Component);i=h&&h.prototype;function j(){var k,l;for(var m=arguments.length,n=Array(m),o=0;o<m;o++)n[o]=arguments[o];return l=(k=i.constructor).call.apply(k,[this].concat(n)),this.state={shouldShowDialog:true},this.$BoostedComponentMainDialogV2ContainerWrapper1=function(p){if(!p)this.setState({shouldShowDialog:false});this.props.onToggle&&this.props.onToggle(p)}.bind(this),l}j.prototype.componentDidMount=function(){var k=this.props,l=k.appID,m=k.boostID,n=k.placement,o=k.targetID;if(this.state.shouldShowDialog)c("BoostedComponentDialogUIActionsV2").autoOpenDialog(false,l,o,m,n)};j.prototype.render=function(){if(!this.state.shouldShowDialog)return null;var k=this.props,l=k.appID,m=k.boostID,n=k.pageID,o=k.placement,p=k.targetID;if(c("BoostedComponentAppIDUtils").isBoostedPostFamily(l))return c("React").createElement(c("BoostedPostMainDialogV2Container.react"),{appID:l,boostID:m,pageID:n,placement:o,targetID:p,useWithoutButton:true,onToggle:this.$BoostedComponentMainDialogV2ContainerWrapper1});return c("React").createElement(c("BoostedActionMainDialogV2Container.react"),{appID:l,boostID:m,pageID:n,placement:o,targetID:p,useWithoutButton:true,onToggle:this.$BoostedComponentMainDialogV2ContainerWrapper1})};f.exports=j}),null);
__d("HiddenPromoteButton.react",["BoostedComponentAppID","BoostedComponentMainDialogV2ContainerWrapper.react","BoostedComponentRef","PageTransitions","React","URI","createCancelableFunction"],(function a(b,c,d,e,f,g){"use strict";var h,i;h=babelHelpers.inherits(j,c("React").Component);i=h&&h.prototype;function j(){var l;(l=i.constructor).call.apply(l,[this].concat(Array.prototype.slice.call(arguments)));k.call(this);var m=this.$HiddenPromoteButton1();this.state={showDialog:!!m}}j.prototype.componentDidMount=function(){c("PageTransitions").registerCompletionCallback(this.updateDialogState)};j.prototype.componentWillUnmount=function(){this.updateDialogState.cancel()};j.prototype.shouldComponentUpdate=function(l,m){return this.state.showDialog!==m.showDialog};j.prototype.$HiddenPromoteButton1=function(){var l=new(c("URI"))(window.location.href).getQueryData();return c("BoostedComponentAppID")[l.boosted_auto_open]};j.prototype.$HiddenPromoteButton2=function(){var l=new(c("URI"))(window.location.href).getQueryData();return l.notif_t||l.ref||c("BoostedComponentRef").AUTO_OPEN_UNKNOWN_SOURCE};j.prototype.render=function(){if(!this.state.showDialog)return null;var l=this.$HiddenPromoteButton1();if(!l)return null;return c("React").createElement(c("BoostedComponentMainDialogV2ContainerWrapper.react"),{appID:l,boostID:"",pageID:this.props.pageID,placement:this.$HiddenPromoteButton2(),targetID:null,onToggle:this.$HiddenPromoteButton3})};var k=function k(){this.state={showDialog:false};this.$HiddenPromoteButton3=function(l){if(!l)this.setState({showDialog:false})}.bind(this);this.updateDialogState=c("createCancelableFunction")(function(){var l=this.$HiddenPromoteButton1();this.setState({showDialog:!!l});c("PageTransitions").registerCompletionCallback(this.updateDialogState)}.bind(this))};f.exports=j}),null);
__d("EventPageletController",["Run"],(function a(b,c,d,e,f,g){var h={_pagelets:{},_initialized:false,register:function i(j){this._pagelets[j.controller]=j.actionContext;if(!this._initialized)c("Run").onLeave(function(){this._pagelets={}}.bind(this))},getPageletNames:function i(){var j=[];for(var k in this._pagelets){if(!Object.prototype.hasOwnProperty.call(this._pagelets,k))continue;j.push(k)}return j},remove:function i(j){j.forEach(function(k){if(Object.prototype.hasOwnProperty.call(this._pagelets,k))delete this._pagelets[k]}.bind(this))}};f.exports=h}),null);
__d("PagesNuxFrameworkTypedLogger",["Banzai","GeneratedLoggerUtils","nullthrows"],(function a(b,c,d,e,f,g){"use strict";function h(){this.clear()}h.prototype.log=function(){c("GeneratedLoggerUtils").log("logger:PagesNuxFrameworkLoggerConfig",this.$PagesNuxFrameworkTypedLogger1,c("Banzai").BASIC)};h.prototype.logVital=function(){c("GeneratedLoggerUtils").log("logger:PagesNuxFrameworkLoggerConfig",this.$PagesNuxFrameworkTypedLogger1,c("Banzai").VITAL)};h.prototype.clear=function(){this.$PagesNuxFrameworkTypedLogger1={};return this};h.prototype.updateData=function(j){this.$PagesNuxFrameworkTypedLogger1=babelHelpers["extends"]({},this.$PagesNuxFrameworkTypedLogger1,j);return this};h.prototype.setEvent=function(j){this.$PagesNuxFrameworkTypedLogger1.event=j;return this};h.prototype.setNuxID=function(j){this.$PagesNuxFrameworkTypedLogger1.nux_id=j;return this};h.prototype.setNuxSurface=function(j){this.$PagesNuxFrameworkTypedLogger1.nux_surface=j;return this};h.prototype.setPageID=function(j){this.$PagesNuxFrameworkTypedLogger1.page_id=j;return this};h.prototype.setVC=function(j){this.$PagesNuxFrameworkTypedLogger1.vc=j;return this};var i={event:true,nux_id:true,nux_surface:true,page_id:true,vc:true};f.exports=h}),null);
__d("ChatTabViewEvents",["Arbiter"],(function a(b,c,d,e,f,g){"use strict";f.exports=new(c("Arbiter"))()}),null);
__d("PageTimelineChainingTypeConstants",[],(function a(b,c,d,e,f,g){f.exports={FANNING:"fanning",FOLLOW:"follow",SHOW_FOLLOW:"show_follow"}}),null);
__d("PagesTimelineChaining",["Arbiter","Banzai","ChatTabViewEvents","CSS","Event","PageLikeConstants","PagesFollowStore","PageTimelineChainingTypeConstants","Run","Style","SubscriptionsHandler","UIPagelet"],(function a(b,c,d,e,f,g){var h=0,i={_recentlyLikedPageIDs:{},_recentlyMessagedPageIDs:{},container:null,_subscriptions:[],_chatSubscriptions:[],_followSubscription:null,_isFollow:false,_shouldShowRelatedPagesOnBounce:false,init:function j(k,l){this.container=k;this._followSubscription=new(c("SubscriptionsHandler"))();this._isFollow=l.isFollow;this._shouldShowRelatedPagesOnBounce=l.shouldShowRelatedPagesOnBounce;c("Run").onLeave(function(){return this._unsubscribe()}.bind(this));if(!this._showChainSuggestions(l.pageID,false)){this._subscriptions=[c("Arbiter").subscribe(c("PageLikeConstants").LIKED,this.onLike.bind(this,l.pageID))];if(l.canFollow)this._followSubscription.addSubscriptions(c("PagesFollowStore").addListener(function(){var m=c("PagesFollowStore").getState();if(!(l.pageID in m))return;if(m[l.pageID]&&!this._isFollow)this._onFollow(l.pageID);this._isFollow=m[l.pageID]}.bind(this)));if(l.enableLikeCheckup)this._subscriptions.push(c("Arbiter").subscribe(c("PageLikeConstants").UNLIKED,this.onUnlike.bind(this)));if(l.onMessageEnabled)this._chatSubscriptions.push(c("ChatTabViewEvents").subscribe("chat-send-to-page",this.onMessage.bind(this,l.pageID)));if(l.shouldShowRelatedPagesOnBounce)window.addEventListener("scroll",this.onScroll.bind(this,l.pageID),false)}},onScroll:function j(k){if(document.documentElement){var l=window.pageYOffset||document.documentElement.scrollTop;if(l<=h){this._showChainSuggestions(k,true);this._unsubscribe()}h=l}},onLike:function j(k,l,m){if(m.profile_id===k&&m.target){this._recentlyLikedPageIDs[k]=true;this._showChainSuggestions(k,false);this._unsubscribe()}},_onFollow:function j(k){this._showChainFollowSuggestions(k);this._unsubscribe()},onMessage:function j(k,l,m){if(m&&m.pageID===k){this._recentlyMessagedPageIDs[k]=true;this._showMessageSuggestions(k);this._unsubscribe()}},onUnlike:function j(k,l){c("UIPagelet").loadFromEndpoint("PagesLikeCheckupPagelet",this.container,{},{displayCallback:this.displayCallback.bind(this)});this._unsubscribe()},displayCallback:function j(k){if(k)k();var l=this.container.firstChild;if(l)c("Style").set(this.container,"height",l.offsetHeight+"px")},_showChainSuggestions:function j(k,l){if(!(k in this._recentlyLikedPageIDs)&&!(this._shouldShowRelatedPagesOnBounce&&l))return false;var m=c("PageTimelineChainingTypeConstants").FANNING;c("UIPagelet").loadFromEndpoint("PagesTimelineChainingPagelet",this.container,{pageID:k,type:m},{displayCallback:this.displayCallback.bind(this)});return true},_showChainFollowSuggestions:function j(k){var l=c("PageTimelineChainingTypeConstants").FOLLOW;c("UIPagelet").loadFromEndpoint("PagesTimelineChainingPagelet",this.container,{pageID:k,type:l},{displayCallback:this.displayCallback.bind(this)});return true},_showMessageSuggestions:function j(k){if(!(k in this._recentlyMessagedPageIDs))return false;c("UIPagelet").loadFromEndpoint("PagesMessageChainingPagelet",this.container,{pageID:k},{displayCallback:this.displayCallback.bind(this)});return true},dismissCallback:function j(k,l,m){c("CSS").hide(this.container);delete this._recentlyLikedPageIDs[l];this._unsubscribe();if(m==="friend_inviter_chaining"){var n="pages_growth_general_analytical_logger",o={id:l,event:"dismiss_carousel",event_target:"friend_inviter_chaining",feature_name:"friend_inviter_chaining_investigate"};c("Banzai").post(n,o)}},attachDismissCallback:function j(k,l,m,n){c("Event").listen(k,"click",this.dismissCallback.bind(this,l,m,n))},_unsubscribe:function j(){if(this._subscriptions.length){this._subscriptions.forEach(function(k){return c("Arbiter").unsubscribe(k)});this._subscriptions=[]}if(this._chatSubscriptions.length){this._chatSubscriptions.forEach(function(k){return c("ChatTabViewEvents").unsubscribe(k)});this._chatSubscriptions=[]}this._followSubscription&&this._followSubscription.release()}};f.exports=i}),null);
__d("PagesNuxFrameworkStore",["BasicFBNux","FluxReduceStore","PageNuxFrameworkActions","PagesNuxDispatcher","PagesNuxFrameworkTypedLogger"],(function a(b,c,d,e,f,g){"use strict";var h,i;h=babelHelpers.inherits(j,c("FluxReduceStore"));i=h&&h.prototype;j.prototype.getInitialState=function(){return{nuxToRender:{},availableNuxes:{},pageID:null,currentSurface:null}};j.prototype.reduce=function(k,l){switch(l.type){case c("PageNuxFrameworkActions").INIT_SURFACE:k.pageID=l.config.pageID;k.currentSurface=l.config.surface;break;case c("PageNuxFrameworkActions").REGISTER_NUX:var m=k.availableNuxes;if(!m[l.config.surface])m[l.config.surface]={};m[l.config.surface][l.config.nuxID]=l.config;k.availableNuxes=m;break;case c("PageNuxFrameworkActions").SHOW_NUX:k.nuxToRender[l.config.surface]=l.config.nuxID;c("BasicFBNux").onView(l.config.nuxID);break;case c("PageNuxFrameworkActions").XOUT:k.nuxToRender[l.config.surface]=null;c("BasicFBNux").onDismiss(l.config.nuxID);break;case c("PageNuxFrameworkActions").HOLD:k.nuxToRender[l.config.surface]=l.config.nuxID;break}if(l.type!==c("PageNuxFrameworkActions").INIT_SURFACE)new(c("PagesNuxFrameworkTypedLogger"))().setEvent(l.type).setNuxID(l.config.nuxID).setPageID(k.pageID).setNuxSurface(l.config.surface).log();return k};function j(){h.apply(this,arguments)}f.exports=new j(c("PagesNuxDispatcher"))}),null);
__d("XPageNuxSelectorAsyncController",["XController"],(function a(b,c,d,e,f,g){f.exports=c("XController").create("/pages/nux_selector/",{page_id:{type:"FBID",required:true},nux_ids:{type:"EnumVector",required:true,enumType:{member:0}},surface:{type:"Enum",required:true,enumType:1}})}),null);
__d("PagesNuxFrameworkHelper",["AsyncRequest","ContextualDialog","PageNuxFrameworkActions","PagesNuxDispatcher","PagesNuxFrameworkStore","Run","XPageNuxSelectorAsyncController"],(function a(b,c,d,e,f,g){"use strict";var h=[];function i(l){h.push(l)}function j(l){return h.indexOf(l)!==-1}var k={_initSurface:function l(m,n){c("PagesNuxDispatcher").dispatch({config:{pageID:m,surface:n},type:c("PageNuxFrameworkActions").INIT_SURFACE});i(n)},_showNux:function l(m,n){var o=c("PagesNuxFrameworkStore").getState().currentSurface;if(!o)return;if(!m.isShown()){m.show();m.subscribe("hide",function(){c("PagesNuxDispatcher").dispatch({type:c("PageNuxFrameworkActions").XOUT,config:{nuxID:n,surface:o}})})}},_setNuxActive:function l(m){if(!m)return;var n=c("PagesNuxFrameworkStore").getState(),o=n.currentSurface;if(!o)return;var p=n.availableNuxes[o][m];if(!p)return;var q=p.showCallBack;if(!q)return;if(p.isReadyForRender===false&&p.contextRef!==undefined){c("PagesNuxDispatcher").dispatch({type:c("PageNuxFrameworkActions").HOLD,config:{nuxID:m,surface:o}});p.contextRef.addEventListener("show",function(){q.apply();c("PagesNuxDispatcher").dispatch({type:c("PageNuxFrameworkActions").SHOW_NUX,config:{nuxID:m,surface:o}})});return}q.apply();c("PagesNuxDispatcher").dispatch({type:c("PageNuxFrameworkActions").SHOW_NUX,config:{nuxID:m,surface:o}})},_pickAndShowNux:function l(){var m=c("PagesNuxFrameworkStore").getState(),n=m.currentSurface;if(!n)return;if(!m.availableNuxes[n])return;var o=m.nuxToRender[n];if(o){k._setNuxActive(o);return}var p=c("XPageNuxSelectorAsyncController").getURIBuilder().setFBID("page_id",m.pageID).setEnumVector("nux_ids",Object.keys(m.availableNuxes[n])).setEnum("surface",n).getURI();new(c("AsyncRequest"))().setHandler(function(q){k._setNuxActive(q.payload)}).setURI(p).send()},registerNux:function l(m,n,o){var p=function p(){return k._showNux(m,n)};c("PagesNuxDispatcher").dispatch({type:c("PageNuxFrameworkActions").REGISTER_NUX,config:{nuxID:n,showCallBack:p,surface:o}})},showNuxAfterLoading:function l(m,n){c("PagesNuxDispatcher").explicitlyRegisterStore(c("PagesNuxFrameworkStore"));k._initSurface(m,n);c("Run").onAfterLoad(function(){return k._pickAndShowNux()})},RegisterNuxWithDependency:function l(m,n,o,p){var q=function q(){return k._showNux(m,n)};c("PagesNuxDispatcher").dispatch({type:c("PageNuxFrameworkActions").REGISTER_NUX,config:{nuxID:n,showCallBack:q,surface:o,contextRef:p}})},showNuxAferComponentLoading:function l(m){var n=j(m);if(!n)return;var o=c("PagesNuxFrameworkStore").getState();if(o.nuxToRender[m])return;this._pickAndShowNux()}};f.exports=k}),null);
__d("PagesManagerUserMessagePrompt",["ChatAppStore","ChatOpenTabEventLogger","FantaTabActions","MercuryIDs","PagesLogger","PagesLoggerEventEnum","PagesLoggerEventTargetEnum","setImmediate"],(function a(b,c,d,e,f,g){"use strict";var h=2e3,i={openTab:function j(k){var l=arguments.length<=1||arguments[1]===undefined?"pages_manager_user_message_prompt":arguments[1],m=arguments.length<=2||arguments[2]===undefined?h:arguments[2];setTimeout(function(){var n;if(c("ChatAppStore").getState().isInitialized)i._openTabAndLog(k,l);else(function(){var o=c("ChatAppStore").addListener(function(){if(c("ChatAppStore").getState().isInitialized){c("setImmediate")(function(){i._openTabAndLog(k,l)});o.remove()}})})()},m)},_openTabAndLog:function j(k,l){var m=c("MercuryIDs").getThreadIDFromUserID(k);c("FantaTabActions").openTab(m,[l]);c("ChatOpenTabEventLogger").logUserAutoOpen(l,k);c("PagesLogger").log(k,c("PagesLoggerEventEnum").IMPRESSION,c("PagesLoggerEventTargetEnum").PAGE_MESSAGE_PROMPT,null,["pages_growth"],{})}};f.exports=i}),null);
__d("EntityPageSubNavigationLogger",["cx","Arbiter","Event","Parent","SubscriptionsHandler","XUISubNavigationLoader"],(function a(b,c,d,e,f,g,h){var i="_2yaa",j=void 0,k=null,l={subscribe:function m(event,n,o){if(!j)j=new(c("Arbiter"))();return j.subscribe(event,n,o)},register:function m(n){if(!k){k=new(c("SubscriptionsHandler"))();k.addSubscriptions(c("XUISubNavigationLoader").onLeave(function(){k&&k.release();k=null}))}k.addSubscriptions(c("Event").listen(n,"click",function(event){var o=event.target;if(o instanceof Node){var p=c("Parent").byClass(o,i);if(p)j&&j.inform("click",p.getAttribute("data-key"))}}))}};f.exports=l}),null);
__d("PagesProfileSidebarLogger",["EntityPageSubNavigationLogger","PagesLogger","PagesLoggerEventEnum","PagesLoggerEventTargetEnum","SubscriptionsHandler","XUISubNavigationLoader"],(function a(b,c,d,e,f,g){var h=null,i={register:function j(k){if(!h){h=new(c("SubscriptionsHandler"))();h.addSubscriptions(c("XUISubNavigationLoader").onLeave(function(){h&&h.release();h=null}))}h.addSubscriptions(c("EntityPageSubNavigationLogger").subscribe("click",function(event,l){var m=l.indexOf("tab_custom_")!==-1?{tab:"tab_custom",app_id:l.replace("tab_custom_","")}:{tab:l};c("PagesLogger").log(k,c("PagesLoggerEventEnum").CLICK,c("PagesLoggerEventTargetEnum").PAGE_TAB_BAR,null,[],m)}))}};f.exports=i}),null);
__d("XSEOEngagementMetricController",["XController"],(function a(b,c,d,e,f,g){f.exports=c("XController").create("/xsemc/",{})}),null);
__d("SEOEngagementMetric",["AsyncRequest","Event","Parent","XSEOEngagementMetricController","setTimeout"],(function a(b,c,d,e,f,g){var h="client_load",i="retain",j="click",k="submit",l=11e3,m={_category:"",_id:"",init:function n(o,p){this._category=o;this._id=p;c("setTimeout")(function(){return this._log(i)}.bind(this),l);c("Event").listen(document,"click",function(q){var r=q.target||q.srcElement;if(c("Parent").byTag(r,"a"))this._log(j);else if(c("Parent").byTag(r,"button"))this._log(k)}.bind(this));c("Event").listen(document,"submit",function(q){return this._log(k)}.bind(this));this._log(h)},_log:function n(event){var o=Date.now()/1e3,p={category:this._category,id:this._id,client_time:o,event:event};c("AsyncRequest").post(c("XSEOEngagementMetricController").getURIBuilder().getURI(),p)}};f.exports=m}),null);
__d("XUISubNavigationItemsAndNavigationShortcutsHighlighting",["cx","Event","DOM","CSS","throttle","ge"],(function a(b,c,d,e,f,g,h){"use strict";var i="_2yaa",j="_2yau",k="_2yap",l="_8ue",m="_4t7n",n="data-endpoint";o.init=function(p){return new o(p)};function o(p){var q=[];for(var r=0;r<p.length;r++){var s=p[r];q=q.concat(c("DOM").scry(s,"div."+i))}for(var t=0;t<q.length;t++){var u=q[t],v=c("DOM").find(u,"a."+j);c("Event").listen(u,"click",c("throttle")(o.removeHighlightingFromAllItemsExceptForURI.bind(this,v.getAttribute(n))))}}o.removeHighlightingFromAllItemsExceptForURI=function(p){var q=c("ge")("entity_sidebar"),r=c("DOM").scry(q,"div."+i);for(var s=0;s<r.length;s++){var t=r[s],u=c("DOM").find(t,"a."+j);if(u.getAttribute(n)!==p){c("CSS").removeClass(t,l);c("CSS").removeClass(t,k);c("CSS").removeClass(t,m)}}};f.exports=o}),null);