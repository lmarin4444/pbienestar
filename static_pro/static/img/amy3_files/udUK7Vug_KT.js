if (self.CavalryLogger) { CavalryLogger.start_js(["uxKYq"]); }

__d("UFIAddCommentController",["Parent","React","ReactDOM","UFIAddComment.react","UFIAddCommentActionType","UFIAsyncWrapper","UFICallbackStore","UFICommentEditIDStore","UFIDispatcher","UFIDispatcherContext.react","UFIFeedbackContext.react","UFINewCommentNotifier"],(function a(b,c,d,e,f,g){"use strict";h.factory=function(j,k){k.rootid=j.id;return new h(j,Object.freeze(k))};function h(j,k){i.call(this);this.$UFIAddCommentController1=j;this.$UFIAddCommentController2=k;this.$UFIAddCommentController3=new(c("UFIDispatcher"))();this.$UFIAddCommentController4={UFICallbackStore:new(c("UFICallbackStore"))(this.$UFIAddCommentController3)};this.$UFIAddCommentController4.UFICallbackStore.on(c("UFIAddCommentActionType").SUBMIT_NEW,function(l){return c("UFINewCommentNotifier").onNewComment(c("Parent").byTag(j,"form"),this.$UFIAddCommentController2,l.comment,l.target,l.replyCommentID,l.timestamp)}.bind(this));this.$UFIAddCommentController5=c("UFICommentEditIDStore").getForInstance(this.$UFIAddCommentController2.instanceid);c("UFICommentEditIDStore").addListener(function(){var l=c("UFICommentEditIDStore").getForInstance(this.$UFIAddCommentController2.instanceid);if(l!=this.$UFIAddCommentController5){this.$UFIAddCommentController5=l;this.render()}}.bind(this));this.render()}h.prototype.render=function(){var j=c("React").createElement(c("UFIDispatcherContext.react"),{dispatcher:this.$UFIAddCommentController3,stores:this.$UFIAddCommentController4},c("React").createElement(c("UFIFeedbackContext.react"),{contextArgs:this.$UFIAddCommentController2,render:this.renderAddComment}));c("ReactDOM").render(c("React").createElement(c("UFIAsyncWrapper"),null,j),this.$UFIAddCommentController1)};h.prototype.disable=function(){this.$UFIAddCommentController4.UFICallbackStore.remove()};var i=function i(){this.renderAddComment=function(j,k){if(this.$UFIAddCommentController5!==null||!k||!k.cancomment||!k.actorforpost)return null;return c("React").createElement(c("UFIAddComment.react"),{viewerActorID:k.actorforpost,targetID:k.ownerid,groupID:k.grouporeventid,initialData:null,ref:null,withoutSeparator:false,editingComment:{},isEditing:false,mentionsDataSource:k.mentionsdatasource,showSendOnEnterTip:k.showsendonentertip,multiCompanyGroupsCount:k.multicompanygroupscount,allowPhotoAttachments:k.allowphotoattachments&&!j.islivestreaming,allowVideoAttachments:k.allowvideoattachments&&!j.islivestreaming,allowStickerAttachments:k.allowstickerattachments&&!j.islivestreaming,allowGifAttachments:k.allowgifattachments&&!j.islivestreaming,allowTipJar:Boolean(k.istipjarenabled&&j.islivestreaming),contextArgs:j,subtitle:k.subtitle,isQAndA:k.isqanda,keepFocus:j.islivestreaming})}.bind(this)};f.exports=h}),null);
__d("TabBar",["ArbiterMixin","ReactDOM","mixin"],(function a(b,c,d,e,f,g){var h,i;h=babelHelpers.inherits(j,c("mixin")(c("ArbiterMixin")));i=h&&h.prototype;function j(k,l,m){"use strict";i.constructor.call(this);l.props=babelHelpers["extends"]({},l.props,{onTabClick:function(n){return this.inform(j.TAB_CLICK,n)}.bind(this)});c("ReactDOM").render(k(l),m)}j.TAB_CLICK="onTabClick";f.exports=j}),null);
__d("TabBarShim",["DOMContainer.react","React","isNode"],(function a(b,c,d,e,f,g){var h=function h(i){var j;if(i.children){j=i.children.map(function(l,m){if(typeof l==="object"&&typeof l.ctor==="function")return h(l);else if(c("isNode")(l)){var n=c("React").createElement(c("DOMContainer.react"),{key:"TabBarShim-"+m},l);return n}else return l});if(j.length===1)j=j[0]}var k=i.ctor;return c("React").createElement(k,i.props,j)};f.exports=h}),null);
__d("VideoChainingToken",["Base64"],(function a(b,c,d,e,f,g){function h(i){"use strict";this.$VideoChainingToken1=i}h.encode=function(i){"use strict";return new h(c("Base64").encode(JSON.stringify(i)))};h.prototype.decode=function(){"use strict";return JSON.parse(c("Base64").decode(this.$VideoChainingToken1))};f.exports=h}),null);
__d("VideoWithImmediateAbortLoading",[],(function a(b,c,d,e,f,g){function h(){"use strict"}h.prototype.enable=function(i){"use strict";this.$VideoWithImmediateAbortLoading1=i;if(i.getStreamingFormat()==="dash"){i.abortLoading();i.registerOption("VideoWithImmediateAbortLoading","isWithImmediateAbortLoading")}};h.prototype.disable=function(){"use strict";if(this.$VideoWithImmediateAbortLoading1.hasOption("VideoWithImmediateAbortLoading","isWithImmediateAbortLoading"))this.$VideoWithImmediateAbortLoading1.unregisterOption("VideoWithImmediateAbortLoading","isWithImmediateAbortLoading");this.$VideoWithImmediateAbortLoading1=null};f.exports=h}),null);
__d("TahoeEllipsisText.react",["DOMContainer.react","LineClamp.react","Link.react","React"],(function a(b,c,d,e,f,g){var h,i,j=c("React").PropTypes;h=babelHelpers.inherits(k,c("React").Component);i=h&&h.prototype;function k(l,m){"use strict";i.constructor.call(this,l,m)}k.prototype.render=function(){"use strict";var l=this.props.seeMoreLink&&this.props.seeMoreText?c("React").createElement(c("Link.react"),{href:this.props.seeMoreLink},this.props.seeMoreText):"\u2026";return c("React").createElement(c("LineClamp.react"),{lines:this.props.lines,lineHeight:this.props.lineHeight,customEllipsisDisableGradient:false,customEllipsis:l,fitHeightToShorterText:this.props.fitHeightToShorterText},c("React").createElement(c("DOMContainer.react"),null,this.props.content))};k.propTypes={content:j.object.isRequired,lines:j.number.isRequired,lineHeight:j.number.isRequired,seeMoreLink:j.string,seeMoreText:j.string,fitHeightToShorterText:j.bool};f.exports=k}),null);