if (self.CavalryLogger) { CavalryLogger.start_js(["MZJfF"]); }

__d("MercuryAttachmentError.react",["fbt","XUINotice.react","XUIText.react","React"],(function a(b,c,d,e,f,g,h){"use strict";var i,j;i=babelHelpers.inherits(k,c("React").Component);j=i&&i.prototype;k.prototype.render=function(){return c("React").createElement(c("XUINotice.react"),{use:"warn"},c("React").createElement(c("XUIText.react"),{size:"small"},h._("No se pudo cargar este archivo adjunto.")))};function k(){i.apply(this,arguments)}f.exports=k}),null);
__d("MercuryAttachmentFile.react",["ix","cx","fbt","Image.react","LeftRight.react","Link.react","MercuryAttachment","React","URI","isLinkshimURI","joinClasses"],(function a(b,c,d,e,f,g,h,i,j){"use strict";var k,l,m=c("React").PropTypes;k=babelHelpers.inherits(n,c("React").PureComponent);l=k&&k.prototype;n.prototype.componentDidMount=function(){this.props.onAttachmentLoad&&this.props.onAttachmentLoad()};n.prototype.$MercuryAttachmentFile1=function(){if(c("isLinkshimURI")(new(c("URI"))(this.props.url)))return this.props.url;else return{url:(this.props.url||"").toString(),shimhash:this.props.shimhash}};n.prototype.$MercuryAttachmentFile2=function(){if(this.props.open_url)return c("React").createElement("div",{className:"_59gs"},c("React").createElement(c("Link.react"),{target:"_blank",href:this.props.open_url},j._("abrir"))," ","\xb7"," ",c("React").createElement(c("Link.react"),{href:this.$MercuryAttachmentFile1(),s:this.props.isSafeToSkipShim?"1":""},j._("descargar")));return c("React").createElement("div",null)};n.prototype.render=function(){var o=c("joinClasses")(c("MercuryAttachment").getAttachIconClass(this.props.type),"_59go _59gq");if(this.props.url)return c("React").createElement(c("LeftRight.react"),{className:o},c("React").createElement(c("Link.react"),{href:this.$MercuryAttachmentFile1(),s:this.props.isSafeToSkipShim?"1":""},c("React").createElement(c("LeftRight.react"),null,c("React").createElement(c("Image.react"),{src:h("86988")}),c("React").createElement("span",{className:"_59gp"},this.props.name))),this.$MercuryAttachmentFile2());return c("React").createElement(c("LeftRight.react"),{className:o},c("React").createElement(c("Image.react"),{src:h("86988")}),c("React").createElement("span",{className:"_59gp"},this.props.name))};function n(){k.apply(this,arguments)}n.propTypes={isSafeToSkipShim:m.bool,name:m.string.isRequired,onAttachmentLoad:m.func,open_url:m.string,rel:m.string,shimhash:m.string,type:m.string.isRequired,url:m.string};f.exports=n}),null);
__d("MercuryAttachmentMalicious.react",["fbt","XUINotice.react","XUIText.react","React"],(function a(b,c,d,e,f,g,h){"use strict";var i,j;i=babelHelpers.inherits(k,c("React").Component);j=i&&i.prototype;k.prototype.render=function(){return c("React").createElement(c("XUINotice.react"),{use:"warn"},c("React").createElement(c("XUIText.react"),{size:"small"},h._("Se marc\u00f3 este archivo adjunto como malicioso.")))};function k(){i.apply(this,arguments)}f.exports=k}),null);
__d("MercuryAttachmentPhoto.react",["ChatImageArrowDirection","ChatImageWithArrow.react","MercuryAttachmentViewer","MercuryIDs","MercuryMessageInfo","MessagesViewerSetID","React","SpotlightMercurySharedMediaViewer.react","URI","getPageIDFromThreadID"],(function a(b,c,d,e,f,g){"use strict";var h,i,j=c("React").PropTypes;h=babelHelpers.inherits(k,c("React").Component);i=h&&h.prototype;function k(){var l,m;for(var n=arguments.length,o=Array(n),p=0;p<n;p++)o[p]=arguments[p];return m=(l=i.constructor).call.apply(l,[this].concat(o)),this.state={newSharedPhotosView:false},this.$MercuryAttachmentPhoto1=function(q){var r=this.props.image,s=true;if(!this.props.hasAttribution&&this.props.count)s=this.props.count===1;var t=this.props.message,u=t.thread_fbid?t.thread_fbid:c("MercuryIDs").getThreadFBIDFromThreadID(t.thread_id),v=new(c("URI"))("/ajax/messaging/attachments/sharedphotos.php").setQueryData({thread_id:u,image_id:r.metadata.fbid}),w=c("MessagesViewerSetID").MESSAGES_VIEW_ALL_IN_THREAD;c("MercuryAttachmentViewer").bootstrapWithConfig({dimensions:r.metadata.dimensions,disablePaging:s,endpoint:v,fbid:r.metadata.fbid,setID:w,src:r.preview_url},null)}.bind(this),this.$MercuryAttachmentPhoto2=function(){var q=this.props.image;if(q&&q.metadata)this.setState({newSharedPhotosView:q.metadata.fbid})}.bind(this),this.$MercuryAttachmentPhoto3=function(){this.setState({newSharedPhotosView:null})}.bind(this),m}k.prototype.componentDidMount=function(){c("MercuryAttachmentViewer").preload();this.props.onAttachmentLoad&&this.props.onAttachmentLoad(this.props.height)};k.prototype.$MercuryAttachmentPhoto4=function(){var l=this.props.message.thread_fbid||this.props.message.thread_id&&c("MercuryIDs").getThreadFBIDFromThreadID(this.props.message.thread_id);return c("React").createElement(c("SpotlightMercurySharedMediaViewer.react"),{onClosePhotoView:this.$MercuryAttachmentPhoto3,photoID:String(this.state.newSharedPhotosView),rootClassName:"",threadID:l,disableForward:false,enableShareToFB:true})};k.prototype.render=function(){var l=c("MercuryMessageInfo").isInbound(this.props.message),m=!!c("getPageIDFromThreadID")(this.props.message.thread_id),n=!this.props.hasAttribution&&!m?this.$MercuryAttachmentPhoto2:this.$MercuryAttachmentPhoto1,o=this.state.newSharedPhotosView?this.$MercuryAttachmentPhoto4():null;return c("React").createElement("div",{onFocus:this.$MercuryAttachmentPhoto5},o,c("React").createElement(c("ChatImageWithArrow.react"),{arrowDirection:l?c("ChatImageArrowDirection").LEFT:c("ChatImageArrowDirection").RIGHT,source:this.props.image.preview_url,height:this.props.height,width:this.props.width,onClick:n,round:!!this.props.round,isLoading:!!this.props.image.preview_uploading}))};k.prototype.$MercuryAttachmentPhoto5=function(event){event.stopPropagation()};k.propTypes={hasAttribution:j.bool,height:j.number,image:j.object.isRequired,message:j.object.isRequired,onAttachmentLoad:j.func,round:j.bool,width:j.number};f.exports=k}),null);
__d("ChatGridImage.react",["cx","Link.react","React","cssURL","emptyFunction","idx"],(function a(b,c,d,e,f,g,h){"use strict";var i,j,k=c("React").PropTypes;i=babelHelpers.inherits(l,c("React").PureComponent);j=i&&i.prototype;function l(){var m,n;for(var o=arguments.length,p=Array(o),q=0;q<o;q++)p[q]=arguments[q];return n=(m=j.constructor).call.apply(m,[this].concat(p)),this.$ChatGridImage1=function(){var r,s=this.props.onClick||c("emptyFunction"),t=(r=this.props)!=null?(r=r.metadata)!=null?r.fbid:r:r;if(t)s(t);else s()}.bind(this),n}l.prototype.render=function(){if(this.props.isLoading||!this.props.source)return c("React").createElement("div",{className:"_4ypb",style:{width:this.props.size,height:this.props.size}});var m=this.props.source||"";return c("React").createElement(c("Link.react"),{onClick:this.$ChatGridImage1},c("React").createElement("div",{className:"_332l",style:{backgroundImage:c("cssURL")(m),width:this.props.size,height:this.props.size}}))};l.propTypes={isLoading:k.bool,metadata:k.object,onClick:k.func,size:k.number.isRequired,source:k.string};f.exports=l}),null);
__d("MercuryAttachmentPhotoGrid.react",["cx","ChatGridImage.react","Grid.react","MercuryAttachmentType","MercuryAttachmentViewer","MercuryIDs","MessagesViewerSetID","React","SpotlightMercurySharedMediaViewer.react","URI","getPageIDFromThreadID"],(function a(b,c,d,e,f,g,h){"use strict";var i,j,k=c("Grid.react").GridItem,l=c("React").PropTypes;i=babelHelpers.inherits(m,c("React").Component);j=i&&i.prototype;function m(){var n,o;for(var p=arguments.length,q=Array(p),r=0;r<p;r++)q[r]=arguments[r];return o=(n=j.constructor).call.apply(n,[this].concat(q)),this.state={newSharedPhotosView:null},this.$MercuryAttachmentPhotoGrid1=function(s,t){var u=this.props.count,v=this.props.message,w=v.thread_fbid?v.thread_fbid:c("MercuryIDs").getThreadFBIDFromThreadID(v.thread_id),x=new(c("URI"))("/ajax/messaging/attachments/sharedphotos.php").setQueryData({thread_id:w,image_id:s.metadata&&s.metadata.fbid}),y=c("MessagesViewerSetID").MESSAGES_VIEW_ALL_IN_THREAD;return function(z){c("MercuryAttachmentViewer").bootstrapWithConfig({dimensions:s.metadata.dimensions,disablePaging:t||u===1,endpoint:x,fbid:s.metadata.fbid,setID:y,src:s.preview_url},null)}}.bind(this),this.$MercuryAttachmentPhotoGrid2=function(s){if(s)this.setState({newSharedPhotosView:s})}.bind(this),this.$MercuryAttachmentPhotoGrid3=function(){this.setState({newSharedPhotosView:null})}.bind(this),o}m.prototype.componentDidMount=function(){c("MercuryAttachmentViewer").preload()};m.prototype.$MercuryAttachmentPhotoGrid4=function(){var n=this.props.message.thread_fbid||this.props.message.thread_id&&c("MercuryIDs").getThreadFBIDFromThreadID(this.props.message.thread_id);return c("React").createElement(c("SpotlightMercurySharedMediaViewer.react"),{onClosePhotoView:this.$MercuryAttachmentPhotoGrid3,photoID:String(this.state.newSharedPhotosView),rootClassName:"",threadID:n,disableForward:false})};m.prototype.render=function(){var n=this.props.images,o=n.length,p=o==2||o==4?2:3,q=Math.floor(this.props.size/p),r=[],s=n.some(function(x){return x.attach_type===c("MercuryAttachmentType").ANIMATED_IMAGE}),t=this.state.newSharedPhotosView?this.$MercuryAttachmentPhotoGrid4():null,u=!!c("getPageIDFromThreadID")(this.props.message.thread_id);for(var v=0;v<n.length;v++){var w=!u?this.$MercuryAttachmentPhotoGrid2:this.$MercuryAttachmentPhotoGrid1(n[v],s);r.push(c("React").createElement(k,{key:v},c("React").createElement(c("ChatGridImage.react"),{isLoading:!!n[v].preview_uploading,onClick:w,metadata:n[v].metadata,size:q,source:n[v].preview_url})))}return c("React").createElement("div",null,t,c("React").createElement(c("Grid.react"),{cols:p,className:"_5b2w",spacing:"_5b2x",alignh:"right"},r))};m.propTypes={images:l.arrayOf(l.object).isRequired,size:l.number.isRequired,message:l.object.isRequired};f.exports=m}),null);
__d("ChatAttachmentAttribution.react",["cx","ImmutableObject","MercuryAttachmentAttribution.react","React"],(function a(b,c,d,e,f,g,h){"use strict";var i,j,k=c("React").PropTypes;i=babelHelpers.inherits(l,c("React").Component);j=i&&i.prototype;l.prototype.componentDidMount=function(){this.props.onAttachmentLoad&&this.props.onAttachmentLoad()};l.prototype.render=function(){return c("React").createElement(c("MercuryAttachmentAttribution.react"),{attachment:this.props.attachment,className:"_1ekr _4i_6"})};function l(){i.apply(this,arguments)}l.propTypes={attachment:k.instanceOf(c("ImmutableObject")),onAttachmentLoad:k.func};f.exports=l}),null);
__d("MercuryAttachmentVideo.react",["cx","ix","ChatAttachmentAttribution.react","ChatImageWithArrow.react","ChatSpeakingSticker.react","CenteredContainer.react","FBOverlayBase.react","FBOverlayContainer.react","FBOverlayElement.react","Image.react","ImmutableObject","MercuryAttachment","MercuryAttachmentViewer","MessengerVideoPlayer.react","React","SpotlightMercurySharedMediaViewer.react","Vector","getPageIDFromThreadID","joinClasses"],(function a(b,c,d,e,f,g,h,i){var j,k,l=c("React").PropTypes;j=babelHelpers.inherits(m,c("React").Component);k=j&&j.prototype;function m(){var n,o;"use strict";for(var p=arguments.length,q=Array(p),r=0;r<p;r++)q[r]=arguments[r];return o=(n=k.constructor).call.apply(n,[this].concat(q)),this.state={newSharedPhotosView:null},this.$MercuryAttachmentVideo1=function(){var s=this.props.duration,t=Math.floor(s/60),u=s%60;if(u<10)return t+":0"+u;return t+":"+u}.bind(this),this.openViewer=function(){var s=this.props,t=s.pageID,u=s.videoID,v=s.videoSize,w=s.videoURI;v=new(c("Vector"))(v.width,v.height);c("MercuryAttachmentViewer").renderVideo({pageID:t,videoID:u,videoSize:v,videoURI:w})}.bind(this),this.$MercuryAttachmentVideo2=function(){if(this.props.videoID)this.setState({newSharedPhotosView:this.props.videoID})}.bind(this),this.$MercuryAttachmentVideo3=function(){this.setState({newSharedPhotosView:null})}.bind(this),this.$MercuryAttachmentVideo5=function(){if(this.props.isChat)return c("React").createElement("div",null,c("React").createElement(c("ChatImageWithArrow.react"),{height:this.props.thumbSize.height,key:"previewImage",round:true,source:this.props.thumbnail,width:this.props.thumbSize.width}),c("React").createElement(c("ChatAttachmentAttribution.react"),{attachment:this.props.attachment,key:"chatAttribution"}));else return c("React").createElement(c("Image.react"),{height:this.props.thumbSize.height,width:this.props.thumbSize.width,src:this.props.thumbnail})}.bind(this),this.$MercuryAttachmentVideo6=function(){if(this.props.isChat)return{};return this.props.thumbSize}.bind(this),o}m.prototype.componentDidMount=function(){"use strict";this.props.onAttachmentLoad&&this.props.onAttachmentLoad();c("MercuryAttachmentViewer").preload()};m.prototype.$MercuryAttachmentVideo4=function(){"use strict";return c("React").createElement(c("SpotlightMercurySharedMediaViewer.react"),{onClosePhotoView:this.$MercuryAttachmentVideo3,photoID:this.state.newSharedPhotosView,rootClassName:"",threadID:this.props.threadFBID,disableForward:false})};m.prototype.$MercuryAttachmentVideo7=function(n,o){"use strict";if(!n.legacy_attachment_id)return null;return c("React").createElement(c("MessengerVideoPlayer.react"),{attachment:this.props.attachment,videoData:n,isInThread:true,isVisible:this.props.isVisible,onClick:o,className:c("joinClasses")(this.props.className,"_n4o _3_om _1wno")})};m.prototype.$MercuryAttachmentVideo8=function(n){"use strict";var o=this.props.thumbSize,p={x:o.width,y:o.height};return{legacy_attachment_id:this.props.videoID,original_dimensions:p,start_muted:true,no_fullscreen:true,hide_controls_on_finish:true,url:this.props.videoURI}};m.prototype.render=function(){"use strict";if(this.props.attachment.metadata&&this.props.attachment.metadata.render_as_sticker&&this.props.isChat)return c("React").createElement(c("ChatSpeakingSticker.react"),{videoURI:this.props.videoURI,videoSize:this.props.videoSize});var n=!!c("getPageIDFromThreadID")(this.props.threadID),o=!n?this.$MercuryAttachmentVideo2:this.openViewer,p=this.state.newSharedPhotosView&&this.props.threadFBID?this.$MercuryAttachmentVideo4():null,q=c("MercuryAttachment").hasAttribution(this.props.attachment),r="clearfix _zow _59go"+(q?" _4yjw":"")+(this.props.isChat?" _3ds5":""),s=this.$MercuryAttachmentVideo8(this.props.attachment),t=this.$MercuryAttachmentVideo7(s,o),u=t?t:c("React").createElement(c("FBOverlayContainer.react"),{className:r,key:"overlayContainer",onClick:o,style:this.$MercuryAttachmentVideo6()},c("React").createElement(c("FBOverlayBase.react"),null,this.$MercuryAttachmentVideo5()),c("React").createElement(c("FBOverlayElement.react"),null,c("React").createElement("div",{className:(!this.props.isChat?"_zox":"")+(q?" _jt3":"")},c("React").createElement("span",{className:"_zoz"},this.$MercuryAttachmentVideo1()))),c("React").createElement(c("FBOverlayElement.react"),null,c("React").createElement(c("CenteredContainer.react"),{className:q?"_jt3":"",vertical:true},c("React").createElement(c("Image.react"),{src:i("27983")}))));if(this.props.isChat)return c("React").createElement("div",null,p,u);return c("React").createElement("div",null,p,u,c("React").createElement(c("ChatAttachmentAttribution.react"),{attachment:this.props.attachment,key:"inboxAttribution"}))};m.propTypes={attachment:l.instanceOf(c("ImmutableObject")),duration:l.number.isRequired,isChat:l.bool,isVisible:l.bool,threadID:l.string,threadFBID:l.string,name:l.string.isRequired,onAttachmentLoad:l.func,pageID:l.number,thumbSize:l.shape({height:l.number,width:l.number}).isRequired,thumbnail:l.string.isRequired,videoSize:l.shape({height:l.number,width:l.number}).isRequired,videoID:l.string.isRequired,videoURI:l.string.isRequired};f.exports=m}),null);
__d("MercuryAttachmentRenderer",["cx","MercuryAttachmentAudioClip.react","ChatAttachmentAttribution.react","EmojiSticker.react","ImmutableObject","MercuryAttachment","MercuryAttachmentFile.react","MercuryAttachmentPhoto.react","MercuryAttachmentPhotoGrid.react","MercuryAttachmentVideo.react","MercuryConfig","MercuryIDs","MercuryShareAttachment.react","MercuryShareAttachmentRenderLocations","MessagingGiftWrapChecker","MessengerFromViewerUtils","MessengerHotLikeUtils","MessengerSupportedEmojiUtils","MessengerWebDriverTestIDs","React","Sticker.react","StickerAssetType","StickerConstants","StoryAttachmentStyle","BootloadedComponent.react","JSResource","QE2Logger","idx","XStickerAssetController"],(function a(b,c,d,e,f,g,h){"use strict";var i=12,j={renderFile:function k(l,m,n){return c("React").createElement(c("MercuryAttachmentFile.react"),{isSafeToSkipShim:l.url_skipshim,name:l.name,onAttachmentLoad:n,open_url:m?null:l.open_url,rel:l.rel,shimhash:l.url_shimhash,type:l.icon_type,url:l.url})},renderAudioClip:function k(l,m,n,o,p){var q=l.metadata.duration/1e3,r=c("MercuryShareAttachmentRenderLocations").CHAT,s=100,t=m?160:400,u=100;if(q>=5)u=(1-Math.pow(10,(q-5)/-30))*(t-s)+s;return[c("React").createElement(c("MercuryAttachmentAudioClip.react"),{customColor:n,duration:l.metadata.duration/1e3,isChat:m,isFromViewer:c("MessengerFromViewerUtils").isFromViewer(o),location:r,key:"audioClip",onAttachmentLoad:p,rootClassName:c("MercuryAttachment").hasAttribution(l)?"_4yjw":"",showHelp:false,src:l.url,width:u}),c("React").createElement(c("ChatAttachmentAttribution.react"),{attachment:new(c("ImmutableObject"))(l),key:"audioAttribution",onAttachmentLoad:p})]},renderVideo:function k(l,m,n,o,p){var q=m?l.metadata.chat_size:l.metadata.inbox_size,r=m?l.metadata.chat_preview:l.metadata.inbox_preview;if(!q||!r)return null;var s=n&&(n.thread_fbid||n.thread_id&&c("MercuryIDs").getThreadFBIDFromThreadID(n.thread_id));return c("React").createElement("div",null,c("React").createElement(c("MercuryAttachmentVideo.react"),{attachment:new(c("ImmutableObject"))(l),duration:l.metadata.duration,isChat:m,isVisible:p,threadID:n&&n.thread_id,threadFBID:s,name:l.name,onAttachmentLoad:o,pageID:l.metadata.pageid,thumbSize:q,thumbnail:r,videoSize:l.metadata.dimensions,videoID:l.metadata.fbid,videoURI:l.url}))},constructStickerComponent:function k(l,m,n,o,p,q){var r=o?"chatScrolled/":"messengerScrolled/";r+=l.thread_id;if(!m){m=c("MessengerHotLikeUtils").getMetadataForHotLike(l.sticker_id);if(!m){var s={},t={height:c("StickerConstants").THREAD_SIZE,width:c("StickerConstants").THREAD_SIZE},u=t.height,v=t.width;s.height=u;s.width=v;s.stickerID=l.sticker_id;s.spriteURI="";s.spriteURI2x="";s.paddedSpriteURI="";s.paddedSpriteURI2x="";m=s}}var w=null;if(m.stickerID)w=m.stickerID.toString();else if(l.sticker_id)w=l.sticker_id.toString();var x=null;if(m.packID)x=m.packID.toString();var y=c("XStickerAssetController").getURIBuilder().setInt("sticker_id",w),z=null,A=null;if(window.devicePixelRatio&&window.devicePixelRatio>1){A=m.paddedSpriteURI2x;z=m.spriteURI2x}else{A=m.paddedSpriteURI;z=m.spriteURI}var B=!!c("MessengerHotLikeUtils").getMetadataForHotLike(w)&&c("MessagingGiftWrapChecker").shouldRenderWithGiftWrap(l);return c("React").createElement(c("Sticker.react"),{accessibilityLabel:m.accessibilityLabel,animationTrigger:"hover",className:B?"_3m7x":"",customColor:q,frameCount:m.frameCount||1,frameRate:m.frameRate||83,framesPerCol:m.framesPerCol||1,framesPerRow:m.framesPerRow||1,onAttachmentLoad:p,onStickerClick:n,packID:x,paddedSpriteURI:A,sourceHeight:m.height,sourceURI:y.setEnum("image_type",c("StickerAssetType").IMAGE).getURI().toString(),sourceWidth:m.width,spriteURI:z,stickerID:w,subscribedThreadID:r,testID:c("MessengerWebDriverTestIDs").STICKER})},constructEmojiLikeAttachment:function k(l,m,n){var o=c("MessengerSupportedEmojiUtils").getNewEmojiData(m.body,l.size),p=o?o.emoji:undefined;if(!o)return null;return c("React").createElement(c("EmojiSticker.react"),{className:"_2poz _ui9",key:"sticker:"+m.message_id,emoji:m.body,emojiImage:p,sourceURI:"",onAttachmentLoad:n})},renderPhotoAttachments:function k(l,m,n,o){var p=l.length;if(!p)return null;var q=m&&m.thread_fbid;if(m&&!q)q=c("MercuryIDs").isLocalThread(m.thread_id)?null:c("MercuryIDs").getThreadFBIDFromThreadID(m.thread_id);if(p===1){var r=l[0],s=c("MercuryAttachment").resizeContain({width:n-i,height:n},{width:r.preview_width,height:r.preview_height});return c("React").createElement("div",{className:"_55pk _59go"+(c("MercuryAttachment").hasAttribution(r)?" _4yjw":"")},c("React").createElement(c("MercuryAttachmentPhoto.react"),{image:r,width:s.width,hasAttribution:c("MercuryAttachment").hasAttribution(r),height:s.height,message:m,onAttachmentLoad:o,round:true}),c("React").createElement(c("ChatAttachmentAttribution.react"),{attachment:new(c("ImmutableObject"))(l[0])}))}return c("React").createElement("div",{className:"_55pk"},c("React").createElement(c("MercuryAttachmentPhotoGrid.react"),{images:l,size:n-i,message:m}))},sortAttachmentsStablyByType:function k(l){var m=[c("MercuryAttachment").isEmojiLikeAttachment,c("MercuryAttachment").isPhotoAttachment,c("MercuryAttachment").isShareAttachment,c("MercuryAttachment").isFileAttachment,c("MercuryAttachment").isErrorAttachment];m.push(function(o){return true});var n=m.map(function(o){return[]});l.forEach(function(o){for(var p=0;p<m.length;p++)if(m[p](o)){n[p].push(o);break}});return Array.prototype.concat.apply([],n)},constructStoryBasedShareAttachment:function k(l,m,n,o,p,q){var r,s,t=c("MercuryShareAttachmentRenderLocations").CHAT,u=m.share&&m.share.style_list&&m.share.style_list[0]===c("StoryAttachmentStyle").CULTURAL_MOMENT_HOLIDAY_CARD,v={maxWidth:o},w=null;if(l&&l.platform_xmd)w=JSON.parse(l.platform_xmd);var x=(r=m)!=null?(r=r.share)!=null?(r=r.messenger_ctas)!=null?(r=r[0])!=null?r.page_id:r:r:r:r,y=(s=m)!=null?(s=s.share)!=null?(s=s.target)!=null?(s=s.items)!=null?(s=s[0])!=null?(s=s.call_to_actions)!=null?(s=s[0])!=null?s.page_id:s:s:s:s:s:s:s,z=x||y,A=z?c("MercuryIDs").getParticipantIDFromUserID(z):l.author,B=c("MessengerFromViewerUtils").isFromViewer(l),C=B?"_fy8":"_fy9";c("QE2Logger").logExposureForUser("messenger_chat_allow_forward_for_shared_attachment");return c("MercuryConfig").MessengerForwardButtonForSharedLinksQE&&c("MercuryAttachment").isShareAttachment(m)&&m.share&&m.share.share_id&&(!m.share.target||!m.share.target.lwa_type)?c("React").createElement("div",null,c("React").createElement("div",{className:C},c("React").createElement(c("BootloadedComponent.react"),{key:"forwardimages:"+m.id,bootloadPlaceholder:c("React").createElement("div",null),bootloadLoader:c("JSResource")("ChatPhotoForwardButton.react").__setRef("MercuryAttachmentRenderer"),attachmentIDs:[m.share.share_id],attachmentTypes:[m.attach_type],isFromViewer:B})),c("React").createElement("div",{className:"_3_om"+(n&&!u?" _3cpq":""),style:v},c("React").createElement(c("MercuryShareAttachment.react"),{attachment:m.share,isSponsored:l.is_sponsored,isVisible:q,location:t,maxWidth:o,messageID:l.message_id,mnMessageType:w&&w.template_type,onComponentLoaded:p,pageID:A,threadID:l.thread_id}))):c("React").createElement("div",{className:"_3_om"+(n&&!u?" _3cpq":""),style:v},c("React").createElement(c("MercuryShareAttachment.react"),{attachment:m.share,isSponsored:l.is_sponsored,isVisible:q,location:t,maxWidth:o,messageID:l.message_id,mnMessageType:w&&w.template_type,onComponentLoaded:p,pageID:A,threadID:l.thread_id}))}};f.exports=j}),null);
__d("MercuryAttachments.react",["cx","MercuryAttachmentRenderer","ImmutableObject","MercuryAttachment","MercuryAttachmentMalicious.react","MercuryAttachmentError.react","MessagingFlowerBorder.react","MessagingGiftWrap.react","MessengerHotLikePreview.react","MessengerWebDriverTestIDs","MNCommerceMessageType","React","SubscriptionsHandler","emptyFunction","joinClasses"],(function a(b,c,d,e,f,g,h){"use strict";var i,j,k=c("React").PropTypes;i=babelHelpers.inherits(l,c("React").Component);j=i&&i.prototype;function l(){var m,n;for(var o=arguments.length,p=Array(o),q=0;q<o;q++)p[q]=arguments[q];return n=(m=j.constructor).call.apply(m,[this].concat(p)),this.$MercuryAttachments1=function(r){this.props.onAttachmentLoad&&this.props.onAttachmentLoad(r)}.bind(this),this.$MercuryAttachments2=null,n}l.prototype.componentDidMount=function(){this.$MercuryAttachments2=new(c("SubscriptionsHandler"))()};l.prototype.componentWillUnmount=function(){this.$MercuryAttachments2&&this.$MercuryAttachments2.release()};l.prototype.$MercuryAttachments3=function(m){if(c("MercuryAttachment").isStickerAttachment(m))return c("MercuryAttachmentRenderer").constructStickerComponent(this.props.message,this.props.attachments[0].metadata,this.props.onStickerClick,this.props.isChat,this.$MercuryAttachments1,this.props.customColor);else if(c("MercuryAttachment").isEmojiLikeAttachment(m)){var n=c("MercuryAttachmentRenderer").constructEmojiLikeAttachment(m,this.props.message,this.$MercuryAttachments1);return n?n:c("React").createElement(c("MercuryAttachmentError.react"),null)}else if(c("MercuryAttachment").isVoiceAttachment(m))return c("MercuryAttachmentRenderer").renderAudioClip(this.props.attachments[0],this.props.isChat,this.props.customColor,this.props.message,this.$MercuryAttachments1);else if(c("MercuryAttachment").isVideoAttachment(m))return c("MercuryAttachmentRenderer").renderVideo(m,this.props.isChat,this.props.message,this.$MercuryAttachments1,this.props.isVisible);else if(c("MercuryAttachment").isShareAttachment(m))return c("MercuryAttachmentRenderer").constructStoryBasedShareAttachment(this.props.message,m,this.props.isChat,this.props.maxWidth,this.$MercuryAttachments1,this.props.isVisible);else if(c("MercuryAttachment").isFileAttachment(m))return c("MercuryAttachmentRenderer").renderFile(m,this.props.isChat,this.$MercuryAttachments1);else if(c("MercuryAttachment").isErrorAttachment(m))return c("React").createElement(c("MercuryAttachmentError.react"),null);return c("React").createElement(c("MercuryAttachmentMalicious.react"),null)};l.prototype.render=function(){if(this.props.message.is_like_preview)return c("React").createElement(c("MessengerHotLikePreview.react"),{isChat:this.props.isChat,key:"hlp:"+this.props.message.like_preview_since,since:this.props.message.like_preview_since,customLike:this.props.message.customLike,customColor:this.props.customColor});if(this.props.attachments.length===0)return c("React").createElement("div",this.props);if(this.props.message.commerce_message_type===c("MNCommerceMessageType").RIDE_INTENT)return c("React").createElement("div",this.props);var m=c("MercuryAttachmentRenderer").renderPhotoAttachments(this.props.attachments.filter(c("MercuryAttachment").isPhotoAttachment),this.props.message,this.props.maxWidth,this.$MercuryAttachments1),n=c("MercuryAttachmentRenderer").sortAttachmentsStablyByType(this.props.attachments.filter(function(p){return!c("MercuryAttachment").isPhotoAttachment(p)})).map(function(p,q){return c("React").createElement("span",{key:q},this.$MercuryAttachments3(p))}.bind(this)),o=this.props.hasFlowerBorder?c("joinClasses")("_337n",this.props.className):this.props.className;return c("React").createElement("div",babelHelpers["extends"]({},this.props,{className:o,"data-testid":c("MessengerWebDriverTestIDs").ATTACHMENT_ROOT}),m,n,this.props.afterDecorators,this.props.renderProgressBar&&this.props.renderProgressBar())};l.propTypes={afterDecorators:k.arrayOf(k.element),attachments:k.array.isRequired,customColor:k.string,customLike:k.object,maxWidth:k.number.isRequired,message:k.instanceOf(c("ImmutableObject")).isRequired,isChat:k.bool,isVisible:k.bool,onAttachmentLoad:k.func,onStickerClick:k.func,onUnwrap:k.func};l.defaultProps={isChat:false,onAttachmentLoad:c("emptyFunction"),onStickerClick:c("emptyFunction")};f.exports=l}),null);