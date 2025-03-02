import os
import json
import datetime
import re
import asyncio
import aiohttp
from html import escape

# Discord'un birebir aynısı olan HTML şablonu
HTML_TEMPLATE = """<!DOCTYPE html><html lang="tr"><head><title>{{channel_name}} - {{server_name}}</title><meta charset=utf-8><meta name=viewport content="width=device-width"><style>@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-normal-400.woff2");font-family:gg sans;font-weight:400;font-style:normal}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-normal-500.woff2");font-family:gg sans;font-weight:500;font-style:normal}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-normal-600.woff2");font-family:gg sans;font-weight:600;font-style:normal}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-normal-700.woff2");font-family:gg sans;font-weight:700;font-style:normal}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-normal-800.woff2");font-family:gg sans;font-weight:800;font-style:normal}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-italic-400.woff2");font-family:gg sans;font-weight:400;font-style:italic}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-italic-500.woff2");font-family:gg sans;font-weight:500;font-style:italic}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-italic-600.woff2");font-family:gg sans;font-weight:600;font-style:italic}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-italic-700.woff2");font-family:gg sans;font-weight:700;font-style:italic}@font-face{src:url("https://cdn.jsdelivr.net/gh/Tyrrrz/DiscordFonts@master/ggsans-italic-800.woff2");font-family:gg sans;font-weight:800;font-style:italic}html,body{margin:0;padding:0;background-color:#36393e;color:#dcddde;font-family:"gg sans","Helvetica Neue",Helvetica,Arial,sans-serif;font-size:17px;font-weight:400;scroll-behavior:smooth}a{color:#00aff4;text-decoration:none}a:hover{text-decoration:underline}img{object-fit:contain;image-rendering:high-quality;image-rendering:-webkit-optimize-contrast}.preamble{display:grid;grid-template-columns:auto 1fr;max-width:100%;padding:1rem}.preamble__guild-icon-container{grid-column:1}.preamble__guild-icon{max-width:88px;max-height:88px}.preamble__entries-container{grid-column:2;margin-left:1rem}.preamble__entry{margin-bottom:0.15rem;color:#ffffff;font-size:1.4rem}.preamble__entry--small{font-size:1rem}.chatlog{padding:1rem 0;width:100%;border-top:1px solid rgba(255,255,255,0.1);border-bottom:1px solid rgba(255,255,255,0.1)}.chatlog__message-group{margin-bottom:1rem}.chatlog__message-container{background-color:transparent;transition:background-color 1s ease}.chatlog__message-container--highlighted{background-color:rgba(114,137,218,0.2)}.chatlog__message-container--pinned{background-color:rgba(249,168,37,0.05)}.chatlog__message{display:grid;grid-template-columns:auto 1fr;padding:0.15rem 0;direction:ltr;unicode-bidi:bidi-override}.chatlog__message:hover{background-color:#32353b}.chatlog__message:hover .chatlog__short-timestamp{display:block}.chatlog__message-aside{grid-column:1;width:72px;padding:0.15rem 0.15rem 0 0.15rem;text-align:center}.chatlog__reply-symbol{height:10px;margin:6px 4px 4px 36px;border-left:2px solid #4f545c;border-top:2px solid #4f545c;border-radius:8px 0 0 0}.chatlog__avatar{width:40px;height:40px;border-radius:50%}.chatlog__short-timestamp{display:none;color:#a3a6aa;font-size:0.75rem;font-weight:500;direction:ltr;unicode-bidi:bidi-override}.chatlog__message-primary{grid-column:2;min-width:0}.chatlog__reply{display:flex;margin-bottom:0.15rem;align-items:center;color:#b5b6b8;font-size:0.875rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.chatlog__reply-avatar{width:16px;height:16px;margin-right:0.25rem;border-radius:50%}.chatlog__reply-author{margin-right:0.3rem;font-weight:600}.chatlog__reply-content{overflow:hidden;text-overflow:ellipsis}.chatlog__reply-link{cursor:pointer}.chatlog__reply-link *{display:inline;pointer-events:none}.chatlog__reply-link .chatlog__markdown-quote{display:inline}.chatlog__reply-link .chatlog__markdown-pre{display:inline}.chatlog__reply-link:hover{color:#ffffff}.chatlog__reply-link:hover *:not(.chatlog__markdown-spoiler){color:inherit}.chatlog__reply-edited-timestamp{margin-left:0.25rem;color:#a3a6aa;font-size:0.75rem;font-weight:500;direction:ltr;unicode-bidi:bidi-override}.chatlog__system-notification-icon{width:18px;height:18px}.chatlog__system-notification-author{font-weight:500;color:#ffffff}.chatlog__system-notification-content{color:#96989d}.chatlog__system-notification-link{font-weight:500;color:#ffffff}.chatlog__system-notification-timestamp{margin-left:0.3rem;color:#a3a6aa;font-size:0.75rem;font-weight:500;direction:ltr;unicode-bidi:bidi-override}.chatlog__system-notification-timestamp a{color:inherit}.chatlog__header{margin-bottom:0.1rem}.chatlog__author{font-weight:500;color:#ffffff}.chatlog__author-tag{position:relative;top:-0.1rem;margin-left:0.3rem;padding:0.05rem 0.3rem;border-radius:3px;background-color:#5865F2;color:#ffffff;font-size:0.625rem;font-weight:500;line-height:1.3}.chatlog__timestamp{margin-left:0.3rem;color:#a3a6aa;font-size:0.75rem;font-weight:500;direction:ltr;unicode-bidi:bidi-override}.chatlog__timestamp a{color:inherit}.chatlog__content{padding-right:1rem;font-size:0.95rem;word-wrap:break-word}.chatlog__edited-timestamp{margin-left:0.15rem;color:#a3a6aa;font-size:0.75rem;font-weight:500}.chatlog__attachment{position:relative;width:fit-content;margin-top:0.3rem;border-radius:3px;overflow:hidden}.chatlog__attachment--hidden{cursor:pointer;box-shadow:0 0 1px 1px rgba(0,0,0,0.1)}.chatlog__attachment--hidden *{pointer-events:none}.chatlog__attachment-spoiler-caption{display:none;position:absolute;left:50%;top:50%;z-index:999;padding:0.4rem 0.8rem;border-radius:20px;transform:translate(-50%,-50%);background-color:rgba(0,0,0,0.9);color:#dcddde;font-size:0.9rem;font-weight:600;letter-spacing:0.05rem}.chatlog__attachment--hidden .chatlog__attachment-spoiler-caption{display:block}.chatlog__attachment--hidden:hover .chatlog__attachment-spoiler-caption{color:#fff}.chatlog__attachment-media{max-width:45vw;max-height:500px;vertical-align:top;border-radius:3px}.chatlog__attachment--hidden .chatlog__attachment-media{filter:blur(44px)}.chatlog__attachment-generic {
  max-width: 520px;
  width: 100%;
  height: auto;
  min-height: 40px;
  padding: 10px;
  border: 1px solid #292b2f;
  border-radius: 3px;
  background-color: #2f3136;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.chatlog__attachment-generic-icon {
  float: left;
  width: 30px;
  height: 40px;
  margin-right: 10px;
}

.chatlog__attachment-generic-info {
  flex: 1;
  overflow: hidden;
}

.chatlog__attachment-generic-name {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  font-weight: 500;
}

.chatlog__attachment-generic-size {
  color: #72767d;
  font-size: 12px;
  margin-top: 4px;
}

/* Embed resimlerinin taşmasını önlemek için */
.chatlog__embed-generic-image {
  max-width: 100%;
  max-height: 300px;
  border-radius: 3px;
  object-fit: contain;
}

/* Tüm embed içeriklerinin taşmasını önle */
.chatlog__embed-content-container {
  max-width: 520px;
  width: 100%;
  overflow: hidden;
}

/* Dosya ekleri için buton stili */
.chatlog__attachment-download-button {
  display: inline-block;
  margin-top: 5px;
  padding: 5px 10px;
  background-color: #4f545c;
  border-radius: 3px;
  font-size: 12px;
  font-weight: 500;
  color: white;
  text-decoration: none;
}

.chatlog__attachment-download-button:hover {
  background-color: #5d6269;
  text-decoration: none;
}

.chatlog__embed{display:flex;margin-top:0.3rem;max-width:520px;width:100%}.chatlog__embed-color-pill{flex-shrink:0;width:0.25rem;border-top-left-radius:3px;border-bottom-left-radius:3px}.chatlog__embed-color-pill--default{background-color:#202225}.chatlog__embed-content-container{display:flex;flex-direction:column;padding:0.5rem 0.6rem;border:1px solid rgba(46,48,54,0.6);border-top-right-radius:3px;border-bottom-right-radius:3px;background-color:rgba(46,48,54,0.3);width:100%}.chatlog__embed-content{display:flex;width:100%}.chatlog__embed-text{flex:1}.chatlog__embed-author-container{display:flex;margin-bottom:0.5rem;align-items:center}.chatlog__embed-author-icon{width:20px;height:20px;margin-right:0.5rem;border-radius:50%}.chatlog__embed-author{color:#ffffff;font-size:0.875rem;font-weight:600;direction:ltr;unicode-bidi:bidi-override}.chatlog__embed-author-link{color:#ffffff}.chatlog__embed-title{margin-bottom:0.5rem;color:#ffffff;font-size:0.875rem;font-weight:600}.chatlog__embed-description{color:#dcddde;font-weight:500;font-size:0.85rem}.chatlog__embed-fields{display:flex;flex-wrap:wrap;gap:0 0.5rem}.chatlog__embed-field{flex:0;min-width:100%;max-width:506px;padding-top:0.6rem;font-size:0.875rem}.chatlog__embed-field--inline{flex:1;flex-basis:auto;min-width:50px}.chatlog__embed-field-name{margin-bottom:0.2rem;color:#ffffff;font-weight:600}.chatlog__embed-field-value{color:#dcddde;font-weight:500}.chatlog__embed-thumbnail{flex:0;max-width:80px;max-height:80px;margin-left:1.2rem;border-radius:3px}.chatlog__embed-images{display:block;margin-top:0.6rem;width:100%}.chatlog__embed-images--single{display:block}.chatlog__embed-image{max-width:100%;max-height:300px;border-radius:3px;object-fit:contain;margin:0 auto;display:block}.chatlog__embed-footer{margin-top:0.6rem;color:#dcddde}.chatlog__embed-footer-icon{width:20px;height:20px;margin-right:0.2rem;border-radius:50%;vertical-align:middle}.chatlog__embed-footer-text{vertical-align:middle;font-size:0.75rem;font-weight:500}.chatlog__embed-invite-container{min-width:320px;padding:0.6rem 0.7rem;border:1px solid rgba(46,48,54,0.6);border-radius:3px;background-color:rgba(46,48,54,0.3)}.chatlog__embed-invite-title{margin:0 0 0.8rem 0;color:#b9bbbe;font-size:0.75rem;font-weight:700;text-transform:uppercase}.chatlog__embed-invite{display:flex}.chatlog__embed-invite-guild-icon{width:50px;height:50px;border-radius:0.85rem}.chatlog__embed-invite-info{margin-left:1rem}.chatlog__embed-invite-guild-name{color:#ffffff;font-weight:600}.chatlog__embed-invite-guild-name a{color:inherit}.chatlog__embed-invite-channel-icon{width:18px;height:18px;vertical-align:bottom}.chatlog__embed-invite-channel-name{font-size:0.9rem;font-weight:600}.chatlog__embed-generic-image{object-fit:contain;object-position:left;max-width:45vw;max-height:500px;vertical-align:top;border-radius:3px}.chatlog__embed-generic-video{object-fit:contain;object-position:left;max-width:45vw;max-height:500px;vertical-align:top;border-radius:3px}.chatlog__embed-generic-gifv{object-fit:contain;object-position:left;max-width:45vw;max-height:500px;vertical-align:top;border-radius:3px}.chatlog__embed-spotify{border:0}.chatlog__embed-twitch{border:0}.chatlog__embed-youtube-container{margin-top:0.6rem}.chatlog__embed-youtube{border:0;border-radius:3px}.chatlog__sticker{width:180px;height:180px}.chatlog__sticker--media{max-width:100%;max-height:100%}.chatlog__reactions{display:flex}.chatlog__reaction{display:flex;margin:0.35rem 0.1rem 0.1rem 0;padding:0.125rem 0.375rem;border:1px solid transparent;border-radius:8px;background-color:#2f3136;align-items:center}.chatlog__reaction:hover{border:1px solid hsla(0,0%,100%,.2);background-color:transparent}.chatlog__reaction-count{min-width:9px;margin-left:0.35rem;color:#b9bbbe;font-size:0.875rem}.chatlog__reaction:hover .chatlog__reaction-count{color:#dcddde}.chatlog__markdown{max-width:100%;line-height:1.3;overflow-wrap:break-word}.chatlog__markdown h1{margin:1rem 0 0.5rem;color:#f2f3f5;font-size:1.5rem;line-height:1}.chatlog__markdown h2{margin:1rem 0 0.5rem;color:#f2f3f5;font-size:1.25rem;line-height:1}.chatlog__markdown h3{margin:1rem 0 0.5rem;color:#f2f3f5;font-size:1rem;line-height:1}.chatlog__markdown h1:first-child,h2:first-child,h3:first-child{margin-top:0.5rem}.chatlog__markdown ul,ol{margin:0 0 0 1rem;padding:0}.chatlog__markdown-preserve{white-space:pre-wrap}.chatlog__markdown-spoiler{background-color:rgba(255,255,255,0.1);padding:0 2px;border-radius:3px}.chatlog__markdown-spoiler--hidden{cursor:pointer;background-color:#202225;color:rgba(0,0,0,0)}.chatlog__markdown-spoiler--hidden:hover{background-color:rgba(32,34,37,0.8)}.chatlog__markdown-spoiler--hidden::selection{color:rgba(0,0,0,0)}.chatlog__markdown-quote{display:flex;margin:0.05rem 0}.chatlog__markdown-quote-border{margin-right:0.5rem;border:2px solid #4f545c;border-radius:3px}.chatlog__markdown-pre{background-color:#2f3136;font-family:"Consolas","Courier New",Courier,monospace;font-size:0.85rem;text-decoration:inherit}.chatlog__markdown-pre--multiline{display:block;margin-top:0.25rem;padding:0.5rem;border:2px solid #282b30;border-radius:5px;color:#b9bbbe}.chatlog__markdown-pre--multiline.hljs{background-color:#2f3136;color:#b9bbbe}.chatlog__markdown-pre--inline{display:inline-block;padding:2px;border-radius:3px}.chatlog__markdown-mention{border-radius:3px;padding:0 2px;background-color:rgba(88,101,242,.3);color:#dee0fc;font-weight:500}.chatlog__markdown-mention:hover{background-color:#5865f2;color:#ffffff}.chatlog__markdown-timestamp{background-color:rgba(255,255,255,0.1);padding:0 2px;border-radius:3px}.chatlog__emoji{width:1.325rem;height:1.325rem;margin:0 0.06rem;vertical-align:-0.4rem}.chatlog__emoji--small{width:1rem;height:1rem}.chatlog__emoji--large{width:2.8rem;height:2.8rem}.postamble{padding:1.25rem}.postamble__entry{color:#ffffff}
/* Embed resim gösterimi için özel stil düzeltmeleri */
.chatlog__embed-image {
  display: block;
  max-width: 100%;
  max-height: 120px; /* Daha küçük boyut */
  margin: 0 auto;
  border-radius: 3px;
  object-fit: contain;
}

.chatlog__embed-images--single {
  width: 100%;
  max-width: 100%;
  margin-top: 0.3rem;
  overflow: hidden;
  border-radius: 3px;
  text-align: center;
}

/* Embed container düzeltmesi */
.chatlog__embed-content-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 0.5rem 0.6rem;
  border: 1px solid rgba(46,48,54,0.6);
  border-top-right-radius: 3px; 
  border-bottom-right-radius: 3px;
  background-color: rgba(46,48,54,0.3);
}

/* YouTube videolarını daha kompakt göster */
.chatlog__embed-youtube {
  width: 100%;
  max-width: 400px;
  height: 200px;
  border: none;
  border-radius: 3px;
}

.chatlog__embed-youtube-container {
  width: 100%;
  margin-top: 0.3rem;
  text-align: center;
}

/* Embed generic image stil düzeltmeleri */
.chatlog__embed-generic-image {
  max-width: 400px;
  max-height: 300px;
  border-radius: 3px;
  object-fit: contain;
}

.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 oranı için */
  height: 0;
  overflow: hidden;
  max-width: 100%;
}

.video-container iframe,
.video-container object,
.video-container embed {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style><link rel=stylesheet href=https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.6/styles/solarized-dark.min.css><script src=https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.15.6/highlight.min.js></script><script>document.addEventListener('DOMContentLoaded',()=>{document.querySelectorAll('.chatlog__markdown-pre--multiline').forEach(e=>hljs.highlightBlock(e));});</script><script src=https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.8.1/lottie.min.js></script><script>document.addEventListener('DOMContentLoaded',()=>{document.querySelectorAll('.chatlog__sticker--media[data-source]').forEach(e=>{const anim=lottie.loadAnimation({container:e,renderer:'svg',loop:true,autoplay:true,path:e.getAttribute('data-source')});anim.addEventListener('data_failed',()=>e.innerHTML='<strong>[Sticker cannot be rendered]</strong>');});});</script><script>function scrollToMessage(event,id){const element=document.getElementById('chatlog__message-container-'+id);if(!element)return;event.preventDefault();element.classList.add('chatlog__message-container--highlighted');window.scrollTo({top:element.getBoundingClientRect().top-document.body.getBoundingClientRect().top-(window.innerHeight/2),behavior:'smooth'});window.setTimeout(()=>element.classList.remove('chatlog__message-container--highlighted'),2000);}function showSpoiler(event,element){if(!element)return;if(element.classList.contains('chatlog__attachment--hidden')){event.preventDefault();element.classList.remove('chatlog__attachment--hidden');}if(element.classList.contains('chatlog__markdown-spoiler--hidden')){event.preventDefault();element.classList.remove('chatlog__markdown-spoiler--hidden');}}</script><svg style=display:none xmlns=http://www.w3.org/2000/svg><defs><symbol id=attachment-icon viewBox="0 0 720 960"><path fill=#f4f5fb d=M50,935a25,25,0,0,1-25-25V50A25,25,0,0,1,50,25H519.6L695,201.32V910a25,25,0,0,1-25,25Z /><path fill=#7789c4 d=M509.21,50,670,211.63V910H50V50H509.21M530,0H50A50,50,0,0,0,0,50V910a50,50,0,0,0,50,50H670a50,50,0,0,0,50-50h0V191Z /><path fill=#f4f5fb d=M530,215a25,25,0,0,1-25-25V50a25,25,0,0,1,16.23-23.41L693.41,198.77A25,25,0,0,1,670,215Z /><path fill=#7789c4 d=M530,70.71,649.29,190H530V70.71M530,0a50,50,0,0,0-50,50V190a50,50,0,0,0,50,50H670a50,50,0,0,0,50-50Z /></symbol><symbol id=join-icon viewBox="0 0 18 18"><path fill=#3ba55c d="m0 8h14.2l-3.6-3.6 1.4-1.4 6 6-6 6-1.4-1.4 3.6-3.6h-14.2" /></symbol><symbol id=leave-icon viewBox="0 0 18 18"><path fill=#ed4245 d="m3.8 8 3.6-3.6-1.4-1.4-6 6 6 6 1.4-1.4-3.6-3.6h14.2v-2" /></symbol><symbol id=call-icon viewBox="0 0 18 18"><path fill=#3ba55c fill-rule=evenodd d="M17.7163041 15.36645368c-.0190957.02699568-1.9039523 2.6680735-2.9957762 2.63320406-3.0676659-.09785935-6.6733809-3.07188394-9.15694343-5.548738C3.08002193 9.9740657.09772497 6.3791404 0 3.3061316v-.024746C0 2.2060575 2.61386252.3152347 2.64082114.2972376c.7110335-.4971705 1.4917101-.3149497 1.80959713.1372281.19320342.2744561 2.19712724 3.2811005 2.42290565 3.6489167.09884826.1608492.14714912.3554431.14714912.5702838 0 .2744561-.07975258.5770327-.23701117.8751101-.1527655.2902036-.65262318 1.1664385-.89862055 1.594995.2673396.3768148.94804468 1.26429792 2.351016 2.66357424 1.39173858 1.39027775 2.28923588 2.07641807 2.67002628 2.34187563.4302146-.2452108 1.3086162-.74238132 1.5972981-.89423205.5447887-.28682915 1.0907006-.31944893 1.4568885-.08661115.3459689.2182151 3.3383754 2.21027167 3.6225641 2.41611376.2695862.19234426.4144887.5399137.4144887.91672846 0 .2969525-.089862.61190215-.2808189.88523346" /></symbol><symbol id=pencil-icon viewBox="0 0 18 18"><path fill=#99aab5 d="m0 14.25v3.75h3.75l11.06-11.06-3.75-3.75zm17.71-10.21c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75z" /></symbol><symbol id=pin-icon viewBox="0 0 18 18"><path fill=#b9bbbe d="m16.908 8.39684-8.29587-8.295827-1.18584 1.184157 1.18584 1.18584-4.14834 4.1475v.00167l-1.18583-1.18583-1.185 1.18583 3.55583 3.55502-4.740831 4.74 1.185001 1.185 4.74083-4.74 3.55581 3.555 1.185-1.185-1.185-1.185 4.1475-4.14836h.0009l1.185 1.185z" /></symbol><symbol id=channel-icon viewBox="0 0 24 24"><path fill=#b9bbbe d="M5.88657 21C5.57547 21 5.3399 20.7189 5.39427 20.4126L6.00001 17H2.59511C2.28449 17 2.04905 16.7198 2.10259 16.4138L2.27759 15.4138C2.31946 15.1746 2.52722 15 2.77011 15H6.35001L7.41001 9H4.00511C3.69449 9 3.45905 8.71977 3.51259 8.41381L3.68759 7.41381C3.72946 7.17456 3.93722 7 4.18011 7H7.76001L8.39677 3.41262C8.43914 3.17391 8.64664 3 8.88907 3H9.87344C10.1845 3 10.4201 3.28107 10.3657 3.58738L9.76001 7H15.76L16.3968 3.41262C16.4391 3.17391 16.6466 3 16.8891 3H17.8734C18.1845 3 18.4201 3.28107 18.3657 3.58738L17.76 7H21.1649C21.4755 7 21.711 7.28023 21.6574 7.58619L21.4824 8.58619C21.4406 8.82544 21.2328 9 20.9899 9H17.41L16.35 15H19.7549C20.0655 15 20.301 15.2802 20.2474 15.5862L20.0724 16.5862C20.0306 16.8254 19.8228 17 19.5799 17H16L15.3632 20.5874C15.3209 20.8261 15.1134 21 14.8709 21H13.8866C13.5755 21 13.3399 20.7189 13.3943 20.4126L14 17H8.00001L7.36325 20.5874C7.32088 20.8261 7.11337 21 6.87094 21H5.88657ZM9.41045 9L8.35045 15H14.3504L15.4104 9H9.41045Z" /></symbol><symbol id=thread-icon viewBox="0 0 24 24"><path fill=#b9bbbe d="M5.43309 21C5.35842 21 5.30189 20.9325 5.31494 20.859L5.99991 17H2.14274C2.06819 17 2.01168 16.9327 2.02453 16.8593L2.33253 15.0993C2.34258 15.0419 2.39244 15 2.45074 15H6.34991L7.40991 9H3.55274C3.47819 9 3.42168 8.93274 3.43453 8.85931L3.74253 7.09931C3.75258 7.04189 3.80244 7 3.86074 7H7.75991L8.45234 3.09903C8.46251 3.04174 8.51231 3 8.57049 3H10.3267C10.4014 3 10.4579 3.06746 10.4449 3.14097L9.75991 7H15.7599L16.4523 3.09903C16.4625 3.04174 16.5123 3 16.5705 3H18.3267C18.4014 3 18.4579 3.06746 18.4449 3.14097L17.7599 7H21.6171C21.6916 7 21.7481 7.06725 21.7353 7.14069L21.4273 8.90069C21.4172 8.95811 21.3674 9 21.3091 9H17.4099L17.0495 11.04H15.05L15.4104 9H9.41035L8.35035 15H10.5599V17H7.99991L7.30749 20.901C7.29732 20.9583 7.24752 21 7.18934 21H5.43309Z" /><path fill=#b9bbbe d="M13.4399 12.96C12.9097 12.96 12.4799 13.3898 12.4799 13.92V20.2213C12.4799 20.7515 12.9097 21.1813 13.4399 21.1813H14.3999C14.5325 21.1813 14.6399 21.2887 14.6399 21.4213V23.4597C14.6399 23.6677 14.8865 23.7773 15.0408 23.6378L17.4858 21.4289C17.6622 21.2695 17.8916 21.1813 18.1294 21.1813H22.5599C23.0901 21.1813 23.5199 20.7515 23.5199 20.2213V13.92C23.5199 13.3898 23.0901 12.96 22.5599 12.96H13.4399Z" /></symbol></defs></svg></head><body><div class=preamble><div class=preamble__guild-icon-container><img class=preamble__guild-icon src="{{server_icon_url}}" alt="Guild icon" loading=lazy></div><div class=preamble__entries-container><div class=preamble__entry>{{server_name}}</div><div class=preamble__entry>{{channel_name}}</div></div></div><div class="chatlog">{{messages}}</div><div class=postamble><div class=postamble__entry>Toplam {{message_count}} mesaj dışa aktarıldı</div><div class=postamble__entry>Timezone: UTC+3</div></div></body></html>"""

# Mesaj şablonunu tam olarak Discord'un kullandığı gibi düzenleyelim
MESSAGE_TEMPLATE = """
<div class=chatlog__message-group>
    <div id=chatlog__message-container-{{message_id}} class=chatlog__message-container data-message-id={{message_id}}>
        <div class=chatlog__message>
            <div class=chatlog__message-aside>
                <img class=chatlog__avatar src="{{avatar_url}}" alt=Avatar loading=lazy>
                <div class=chatlog__short-timestamp title="{{timestamp_full}}">{{timestamp_short}}</div>
            </div>
            <div class=chatlog__message-primary>
                {{reply_html}}
                <div class=chatlog__header>
                    <span class=chatlog__author title="{{username}}" data-user-id={{user_id}}>{{username}}</span>
                    {{author_tag}}
                    <span class=chatlog__timestamp title="{{timestamp_full}}"><a href=#chatlog__message-container-{{message_id}}>{{timestamp_readable}}</a></span>
                </div>
                <div class="chatlog__content chatlog__markdown">
                    <span class=chatlog__markdown-preserve>{{content}}</span>
                    {{edited_timestamp}}
                </div>
                {{attachments}}
                {{embeds}}
            </div>
        </div>
    </div>
</div>
"""

# Yanıt şablonu
REPLY_TEMPLATE = """
<div class=chatlog__reply>
    <img class=chatlog__reply-avatar src="{{reply_avatar_url}}" alt=Avatar loading=lazy>
    <span class=chatlog__reply-author>{{reply_username}}</span>
    <span class=chatlog__reply-content>{{reply_content}}</span>
            </div>
"""

# Ekler
ATTACHMENT_TEMPLATE = """
<div class=chatlog__attachment>
    <a href="{{attachment_url}}" target="_blank">
        <img class=chatlog__attachment-media src="{{attachment_url}}" alt="Image attachment" title="Image: {{attachment_filename}} ({{attachment_size}})" loading=lazy>
    </a>
            </div>
"""

# Embed şablonunu Discord'un gerçek yapısına uygun şekilde yeniden yapılandırıyoruz
EMBED_TEMPLATE = """
<div class="chatlog__embed">
    <div class="chatlog__embed-color-pill" style="background-color: {{embed_color}}"></div>
    <div class="chatlog__embed-content-container">
        <div class="chatlog__embed-content">
            <div class="chatlog__embed-text">
                {{embed_author}}
                {{embed_title}}
                {{embed_description}}
                {{embed_fields}}
            </div>
            {{embed_thumbnail}}
        </div>
        {{embed_footer}}
        {{embed_image}}
        {{embed_youtube}}
    </div>
</div>
"""

# YouTube embed container şablonu
YOUTUBE_EMBED_TEMPLATE = """
<div class="video-container">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/{{video_id}}" frameborder="0" allowfullscreen></iframe>
</div>
"""

# Image embed şablonu - bu doğrudan embed içinde kullanılacak
EMBED_IMAGE_TEMPLATE = """
<div class="chatlog__embed-images chatlog__embed-images--single">
    <img class="chatlog__embed-image" src="{{image_url}}" alt="Embedded image" loading="lazy">
</div>
"""

# Renk üretmek için yardımcı fonksiyon
def get_user_color(user_id):
    colors = [
        "#1abc9c", "#2ecc71", "#3498db", "#9b59b6",
        "#e91e63", "#f1c40f", "#e67e22", "#e74c3c"
    ]
    return colors[int(user_id) % len(colors)]

# Mesaj içeriğini düzenlemek için fonksiyon
def format_message_content(content):
    if not content:
        return "<i>Bu mesajda içerik yok</i>"
    
    try:
        # Önce HTML özel karakterlerini kaçır
        escaped_content = escape(content)
        
        # Temel Discord formatlamalarını uygula
        # Kullanıcı ve kanal mentionlarını vurgula
        formatted_content = re.sub(r'&lt;@!?(\d+)&gt;', r'<span class="chatlog__markdown-mention">@kullanıcı</span>', escaped_content)
        formatted_content = re.sub(r'&lt;#(\d+)&gt;', r'<span class="chatlog__markdown-mention">#kanal</span>', formatted_content)
        
        # Emojileri işle - $ işaretini kullanmadan doğrudan emoji adını göster
        formatted_content = re.sub(r'&lt;:([a-zA-Z0-9_]+):(\d+)&gt;', r'<span class="chatlog__emoji">:\1:</span>', formatted_content)
        
        # Kod bloklarını işle - DOTALL bayrağını kullanarak çok satırlı kod bloklarını düzgün işle
        formatted_content = re.sub(r'```([a-zA-Z0-9]*)\n(.*?)\n```', r'<div class="chatlog__markdown-pre chatlog__markdown-pre--multiline">\2</div>', formatted_content, flags=re.DOTALL)
        
        # Satır içi kodları işle
        formatted_content = re.sub(r'`(.*?)`', r'<code class="chatlog__markdown-pre chatlog__markdown-pre--inline">\1</code>', formatted_content)
        
        # Kalın, italik ve üstü çizili metinleri işle
        formatted_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_content)
        formatted_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_content)
        formatted_content = re.sub(r'~~(.*?)~~', r'<del>\1</del>', formatted_content)
        
        # Bağlantıları işle
        formatted_content = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', formatted_content)
        
        # Yeni satırları işle
        formatted_content = formatted_content.replace('\n', '<br>')
        
        return formatted_content
    except Exception as e:
        print(f"Mesaj içeriği işlenirken hata: {str(e)}")
        return f"<pre>{escape(content)}</pre>"

class DiscordSelfBotExporter:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://discord.com/api/v9"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    async def start(self):
        # HTTP oturumu başlat
        self.session = aiohttp.ClientSession(headers={
            "Authorization": self.token,
            "User-Agent": self.user_agent,
            "Content-Type": "application/json"
        })
        
        try:
            # Kullanıcı bilgisini al
            await self.get_user_info()
            
            # Özel mesaj ve sunucu seçeneği sun
            print("\n[0] Özel Mesajlar (DM)")
            
            # Sunucuları al
            await self.get_guilds()
            
            # Kullanıcıdan sunucu veya DM seçmesini iste
            choice_index = await self.choose_option()
            
            if choice_index == 0:  # DM seçildi
                await self.get_dm_channels()
                channel_index = await self.choose_dm_channel()
                await self.export_dm_messages(channel_index)
            else:  # Sunucu seçildi
                guild_index = choice_index - 1  # 0 DM için ayrıldı
                await self.get_channels(guild_index)
                channel_index = await self.choose_channel()
                await self.export_messages(channel_index)
        except Exception as e:
            print(f"\nBir hata oluştu: {e}")
        finally:    
            # Oturumu kapat
            await self.session.close()
            print("\nİşlem tamamlandı. Oturum kapatıldı.")

    async def get_user_info(self):
        try:
            async with self.session.get(f"{self.api_url}/users/@me") as response:
                if response.status == 200:
                    self.user = await response.json()
                    print(f"\nHoş geldiniz {self.user['username']}!")
                else:
                    print(f"Kullanıcı bilgisi alınamadı. Hata kodu: {response.status}")
                    if response.status == 401:
                        print("Token geçersiz. Lütfen doğru bir kullanıcı tokeni giriniz.")
                        raise Exception("Geçersiz token")
        except Exception as e:
            print(f"Hata: {e}")
            raise

    async def get_guilds(self):
        try:
            async with self.session.get(f"{self.api_url}/users/@me/guilds") as response:
                if response.status == 200:
                    self.guilds = await response.json()
                    print("\nSunucular:")
                    for i, guild in enumerate(self.guilds, 1):  # 1'den başlat (0 DM için ayrıldı)
                        print(f"[{i}] {guild['name']}")
                else:
                    print(f"Sunucular alınamadı. Hata kodu: {response.status}")
                    raise Exception("Sunucular alınamadı")
        except Exception as e:
            print(f"Hata: {e}")
            raise

    async def choose_option(self):
        while True:
            try:
                choice = int(input("\nSeçim yapın (0=DM, 1-n=Sunucu): "))
                if choice == 0:
                    return 0  # DM seçildi
                elif 1 <= choice <= len(self.guilds):
                    return choice  # Sunucu seçildi
                else:
                    print("Geçersiz seçim. Lütfen listeden bir index numarası girin.")
            except ValueError:
                print("Lütfen bir sayı girin.")

    async def get_dm_channels(self):
        try:
            async with self.session.get(f"{self.api_url}/users/@me/channels") as response:
                if response.status == 200:
                    all_channels = await response.json()
                    # Sadece DM kanallarını filtrele (type 1)
                    self.dm_channels = [channel for channel in all_channels if channel['type'] in [1, 3]]  # 1=DM, 3=Grup DM
                    
                    print("\nÖzel Mesajlar:")
                    for i, channel in enumerate(self.dm_channels):
                        if channel['type'] == 1:  # DM
                            # DM kanalında ilk recipient kullanıcı adını al
                            recipient = channel['recipients'][0]
                            print(f"[{i}] {recipient['username']}")
                        else:  # Grup DM
                            name = channel.get('name', 'Grup Sohbeti')
                            print(f"[{i}] {name} (Grup)")
                else:
                    print(f"Özel mesaj kanalları alınamadı. Hata kodu: {response.status}")
                    raise Exception("DM kanalları alınamadı")
        except Exception as e:
            print(f"Hata: {e}")
            raise

    async def choose_dm_channel(self):
        while True:
            try:
                choice = int(input("\nSohbet seçin (index numarası): "))
                if 0 <= choice < len(self.dm_channels):
                    return choice
                else:
                    print("Geçersiz seçim. Lütfen listeden bir index numarası girin.")
            except ValueError:
                print("Lütfen bir sayı girin.")

    async def get_channels(self, guild_index):
        guild_id = self.guilds[guild_index]['id']
        self.selected_guild = self.guilds[guild_index]
        
        try:
            async with self.session.get(f"{self.api_url}/guilds/{guild_id}/channels") as response:
                if response.status == 200:
                    all_channels = await response.json()
                    # Sadece metin kanallarını filtrele (type 0)
                    self.channels = [channel for channel in all_channels if channel['type'] == 0]
                    print("\nKanallar:")
                    for i, channel in enumerate(self.channels):
                        print(f"[{i}] {channel['name']}")
                else:
                    print(f"Kanallar alınamadı. Hata kodu: {response.status}")
                    raise Exception("Kanallar alınamadı")
        except Exception as e:
            print(f"Hata: {e}")
            raise

    async def choose_channel(self):
        while True:
            try:
                choice = int(input("\nKanal seçin (index numarası): "))
                if 0 <= choice < len(self.channels):
                    return choice
                else:
                    print("Geçersiz seçim. Lütfen listeden bir index numarası girin.")
            except ValueError:
                print("Lütfen bir sayı girin.")

    async def export_dm_messages(self, channel_index):
        channel = self.dm_channels[channel_index]
        channel_id = channel['id']
        
        # DM adını belirle
        if channel['type'] == 1:  # Bireysel DM
            recipient = channel['recipients'][0]
            channel_name = recipient['username']
            server_name = f"Özel Mesaj: {channel_name}"
            channel_icon = "@"
        else:  # Grup DM
            channel_name = channel.get('name', 'Grup Sohbeti')
            server_name = "Grup Sohbeti"
            channel_icon = "@"
        
        print(f"\n'{channel_name}' ile olan mesajlar alınıyor...")
        
        await self._export_messages(channel_id, channel_name, server_name, channel_icon)

    async def export_messages(self, channel_index):
        channel = self.channels[channel_index]
        channel_id = channel['id']
        channel_name = channel['name']
        server_name = self.selected_guild['name']
        channel_icon = "#"
        
        print(f"\n'{channel_name}' kanalındaki mesajlar alınıyor...")
        
        await self._export_messages(channel_id, channel_name, server_name, channel_icon)

    async def _export_messages(self, channel_id, channel_name, server_name, channel_icon):
        messages = []
        last_message_id = None
        
        # Mesaj sayısı limitini kaldır - tüm mesajları al
        request_count = 0
        
        print(f"\n'{channel_name}' kanalındaki mesajlar alınıyor...")
        print("İlerleme: ", end="", flush=True)
        
        # Eşzamanlı istek sayısını artırmak için bir havuz oluştur
        semaphore = asyncio.Semaphore(15)  # Aynı anda 15 istek yapabilir
        
        async def fetch_messages(before_id=None):
            url = f"{self.api_url}/channels/{channel_id}/messages?limit=100"  # Discord API maksimum 100 mesaj döndürür
            if before_id:
                url += f"&before={before_id}"
            
            async with semaphore:
                try:
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status == 429:  # Rate limit
                            rate_data = await response.json()
                            retry_after = rate_data.get('retry_after', 1)
                            print(f"\nRate limit'e takıldık. {retry_after} saniye bekleniyor...")
                            await asyncio.sleep(retry_after)
                            # Tekrar dene
                            return await fetch_messages(before_id)
                        elif response.status == 503:  # Service Unavailable
                            print(f"\n503 hatası: Sunucu geçici olarak hizmet veremiyor. 3 saniye bekleniyor...")
                            await asyncio.sleep(3)
                            return await fetch_messages(before_id)
                        else:
                            print(f"\nMesajlar alınamadı. Hata kodu: {response.status}")
                            return []
                except Exception as e:
                    print(f"\nHata: {e}")
                    await asyncio.sleep(0.5)
                    return await fetch_messages(before_id)  # Tekrar dene
        
        # İlk batch'i al
        batch = await fetch_messages()
        if batch:
            messages.extend(batch)
            last_message_id = batch[-1]['id']
            print(f"{len(messages)} ", end="", flush=True)
        
        # Kalan mesajları akıllı bir şekilde al
        while batch and len(batch) == 100:
            # Her seferinde bir istek yap
            batch = await fetch_messages(last_message_id)
            
            if batch and len(batch) > 0:
                messages.extend(batch)
                last_message_id = batch[-1]['id']
                print(f"{len(messages)} ", end="", flush=True)
            else:
                break
            
            # Her istekten sonra çok kısa bir bekleme ekle - 0.2 saniye
            await asyncio.sleep(0.2)  # Rate limit'e takılmamak için her istekten sonra 200ms bekle
            
            # Her 20 istekte bir biraz daha uzun bekle
            request_count += 1
            if request_count % 20 == 0:
                await asyncio.sleep(0.5)  # Her 20 istekte bir 500ms bekle
            if request_count % 10 == 0:
                await asyncio.sleep(0.5)  # Her 10 istekte bir 500ms bekle
        
        print("✓")  # İşlem tamamlandı
        
        if messages:
            # Mesajları tarih sırasına göre sırala (eskiden yeniye)
            print(f"\nToplam {len(messages)} mesaj alındı. Sıralanıyor...")
            messages.sort(key=lambda x: x['timestamp'])  # Eskiden yeniye sırala
            
            try:
                # HTML çıktısını oluştur
                print("HTML oluşturuluyor...")
                html_content = self.generate_html(channel_name, server_name, channel_icon, messages)
                
                # Dosyayı kaydet
                filename = f"{server_name}-{channel_name}.html"
                # Dosya adından geçersiz karakterleri kaldır
                filename = re.sub(r'[\\/*?:"<>|]', "", filename)
                
                print(f"Dosya kaydediliyor: {filename}")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"\nMesajlar başarıyla kaydedildi: {filename}")
            except Exception as e:
                print(f"\nHTML oluşturulurken hata: {e}")
        else:
            print("Hiç mesaj bulunamadı veya alınamadı.")

    def generate_html(self, channel_name, server_name, channel_icon, messages):
        try:
            messages_html = []
            
            # Timestamp formatlarını ayarla
            timestamp_formats = {
                'full': '%d %B %Y %A %H:%M',
                'readable': '%d.%m.%Y %H:%M',
                'short': '%H:%M'
            }
            
            # Sunucu simgesi URL'sini ayarla
            server_icon_url = "https://cdn.discordapp.com/embed/avatars/0.png"
            
            if hasattr(self, 'selected_guild') and self.selected_guild and self.selected_guild.get('icon'):
                server_icon_url = f"https://cdn.discordapp.com/icons/{self.selected_guild.get('id', '')}/{self.selected_guild.get('icon', '')}?size=512"
            
            # Mesaj ID'lerini ve içeriklerini hızlı erişim için map'e al
            message_map = {message['id']: message for message in messages}
            
            # Mesajları gruplamak için değişkenler
            current_author_id = None
            current_timestamp = None
            
            # Her bir mesajı işle
            for i, message in enumerate(messages):
                try:
                    # Mesaj zaman damgasını işle
                    timestamp = datetime.datetime.fromisoformat(message['timestamp'].replace('Z', '+00:00'))
                    timestamp_full = timestamp.strftime(timestamp_formats['full'])
                    timestamp_readable = timestamp.strftime(timestamp_formats['readable'])
                    timestamp_short = timestamp.strftime(timestamp_formats['short'])
                    
                    # Kullanıcı profilini al
                    user = message.get('author', {})
                    username = escape(user.get('username', 'Bilinmeyen Kullanıcı'))
                    user_id = user.get('id', '0')
                    
                    # Aynı kullanıcının peş peşe mesajlarını grupla
                    # Eğer aynı kullanıcı 5 dakika içinde mesaj gönderdiyse ve önceki mesajdan hemen sonraysa
                    is_continued = False
                    if i > 0 and user_id == current_author_id:
                        prev_timestamp = datetime.datetime.fromisoformat(messages[i-1]['timestamp'].replace('Z', '+00:00'))
                        time_diff = (timestamp - prev_timestamp).total_seconds()
                        # 5 dakikadan (300 saniye) az zaman geçtiyse grupla
                        if time_diff < 300:
                            is_continued = True
                    
                    current_author_id = user_id
                    current_timestamp = timestamp
                    
                    # Eğer devam eden bir mesajsa, sadece içeriği göster
                    if is_continued:
                        # Mesaj içeriğini formatlayarak işle
                        content = format_message_content(message.get('content', ''))
                        
                        # Düzenleme bilgisi
                        edited_timestamp = ""
                        if message.get('edited_timestamp'):
                            edited_time = datetime.datetime.fromisoformat(message['edited_timestamp'].replace('Z', '+00:00'))
                            edited_readable = edited_time.strftime(timestamp_formats['readable'])
                            edited_timestamp = f'<span class="chatlog__edited-timestamp">(düzenlendi: {edited_readable})</span>'
                        
                        # Ekleri işle
                        attachments = self.format_attachments(message.get('attachments', []))
                        
                        # Embedleri işle
                        embeds = self.format_embeds(message.get('embeds', []))
                        
                        # Devam eden mesaj için basit şablon
                        continued_message = f"""
                        <div id=chatlog__message-container-{message['id']} class=chatlog__message-container data-message-id={message['id']}>
                            <div class=chatlog__message>
                                <div class=chatlog__message-aside>
                                    <div class=chatlog__short-timestamp title="{timestamp_full}">{timestamp_short}</div>
                                </div>
                                <div class=chatlog__message-primary>
                                    <div class="chatlog__content chatlog__markdown">
                                        <span class=chatlog__markdown-preserve>{content}</span>
                                        {edited_timestamp}
                                    </div>
                                    {attachments}
                                    {embeds}
                                </div>
                            </div>
                        </div>
                        """
                        messages_html.append(continued_message)
                        continue
                    
                    # Avatar URL'sini al
                    if user.get('avatar'):
                        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user.get('avatar')}?size=128"
                    else:
                        avatar_url = f"https://cdn.discordapp.com/embed/avatars/{int(user_id) % 5}.png"
                    
                    # Kullanıcı rengi belirle
                    author_color = get_user_color(user_id)
                    
                    # Kullanıcı etiketi (örn. "BOT" rozeti)
                    author_tag = ""
                    if user.get('bot'):
                        author_tag = '<span class="chatlog__author-tag">BOT</span>'
                    
                    # Düzenleme bilgisi
                    edited_timestamp = ""
                    if message.get('edited_timestamp'):
                        edited_time = datetime.datetime.fromisoformat(message['edited_timestamp'].replace('Z', '+00:00'))
                        edited_readable = edited_time.strftime(timestamp_formats['readable'])
                        edited_timestamp = f'<span class="chatlog__edited-timestamp">(düzenlendi: {edited_readable})</span>'
                    
                    # Mesaj içeriğini formatlayarak işle
                    content = format_message_content(message.get('content', ''))
                    
                    # Yanıt bilgisini işle
                    reply_html = ""
                    if message.get('referenced_message'):
                        ref_message = message.get('referenced_message')
                        ref_user = ref_message.get('author', {})
                        ref_username = escape(ref_user.get('username', 'Bilinmeyen Kullanıcı'))
                        
                        if ref_user.get('avatar'):
                            ref_avatar_url = f"https://cdn.discordapp.com/avatars/{ref_user.get('id', '0')}/{ref_user.get('avatar')}?size=16"
                        else:
                            ref_avatar_url = f"https://cdn.discordapp.com/embed/avatars/{int(ref_user.get('id', '0')) % 5}.png"
                        
                        ref_content = ref_message.get('content', '')
                        if len(ref_content) > 50:
                            ref_content = ref_content[:47] + "..."
                        ref_content = escape(ref_content)
                        
                        # Özel değiştirme yöntemi kullanarak süslü parantezleri sadece yer tutucular için değiştir
                        temp_reply = REPLY_TEMPLATE
                        temp_reply = temp_reply.replace("{{reply_avatar_url}}", ref_avatar_url)
                        temp_reply = temp_reply.replace("{{reply_username}}", ref_username)
                        temp_reply = temp_reply.replace("{{reply_content}}", ref_content)
                        reply_html = temp_reply
                    
                    # Ekleri işle
                    attachments = self.format_attachments(message.get('attachments', []))
                    
                    # Embedleri işle
                    embeds = self.format_embeds(message.get('embeds', []))
                    
                    # Özel değiştirme yöntemi kullanarak mesaj şablonunu işle
                    temp_message = MESSAGE_TEMPLATE
                    temp_message = temp_message.replace("{{message_id}}", message['id'])
                    temp_message = temp_message.replace("{{avatar_url}}", avatar_url)
                    temp_message = temp_message.replace("{{username}}", username)
                    temp_message = temp_message.replace("{{user_id}}", user_id)
                    temp_message = temp_message.replace("{{author_color}}", author_color)
                    temp_message = temp_message.replace("{{author_tag}}", author_tag)
                    temp_message = temp_message.replace("{{timestamp_full}}", timestamp_full)
                    temp_message = temp_message.replace("{{timestamp_readable}}", timestamp_readable)
                    temp_message = temp_message.replace("{{timestamp_short}}", timestamp_short)
                    temp_message = temp_message.replace("{{content}}", content)
                    temp_message = temp_message.replace("{{edited_timestamp}}", edited_timestamp)
                    temp_message = temp_message.replace("{{reply_html}}", reply_html)
                    temp_message = temp_message.replace("{{attachments}}", attachments)
                    temp_message = temp_message.replace("{{embeds}}", embeds)
                    
                    messages_html.append(temp_message)
                except Exception as e:
                    print(f"Bir mesaj işlenirken hata: {str(e)}")
                    messages_html.append(f'<div style="padding:10px;margin:5px 0;background:#500;color:white;border-radius:5px">Mesaj işlenirken hata: {escape(str(e))}</div>')
            
            # HTML çıktısını oluşturmadan önce güvenli karakter dönüşümlerini yap
            safe_server_name = escape(server_name)
            safe_channel_name = escape(channel_name)
            
            # Mesaj sayısını güncelle
            message_count = len(messages)
            export_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
            
            # Ana HTML şablonunda yer tutucuları doğrudan değiştir (format() kullanmadan)
            base_html = HTML_TEMPLATE
            base_html = base_html.replace("{{server_name}}", safe_server_name)
            base_html = base_html.replace("{{channel_name}}", safe_channel_name)
            base_html = base_html.replace("{{server_icon_url}}", server_icon_url)
            base_html = base_html.replace("{{messages}}", "".join(messages_html))
            base_html = base_html.replace("{{message_count}}", str(message_count))
            base_html = base_html.replace("{{export_time}}", export_time)
            
            return base_html
        except Exception as e:
            import traceback
            print(f"HTML oluşturulurken genel hata: {str(e)}")
            print(traceback.format_exc())  # Daha detaylı hata bilgisi
            
            # Basit bir hata sayfası döndür
            return f"""<!DOCTYPE html><html><head><title>Discord Mesajları</title><meta charset="utf-8"></head>
            <body style="background:#36393e;color:white;font-family:Arial,sans-serif;padding:20px">
                <h1>{escape(server_name)}</h1>
                <h2>{escape(channel_name)}</h2>
                <p>Mesajlar {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')} tarihinde kaydedildi</p>
                <p>Toplam {len(messages)} mesaj</p>
                <p>HATA: {escape(str(e))}</p>
            </body></html>"""

    def format_attachments(self, attachments):
        if not attachments:
            return ""
        
        attachments_html = ""
        
        for attachment in attachments:
            try:
                filename = attachment.get('filename', 'Ek')
                url = attachment.get('url', attachment.get('proxy_url', ''))
                size = attachment.get('size', 0)
                size_text = self.format_bytes(size)
                
                # Dosya türünü belirle
                is_image = any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'])
                is_video = any(filename.lower().endswith(ext) for ext in ['.mp4', '.webm', '.mov'])
                is_audio = any(filename.lower().endswith(ext) for ext in ['.mp3', '.wav', '.ogg', '.flac'])
                
                # Dosya uzantısını al
                file_ext = filename.split('.')[-1].lower() if '.' in filename else ''
                
                if is_image:
                    # Resim dosyaları için
                    attachment_html = f"""
                    <div class="chatlog__attachment">
                        <a href="{url}" target="_blank">
                            <img class="chatlog__attachment-media" src="{url}" alt="{escape(filename)}" title="{escape(filename)} ({size_text})" loading="lazy">
                        </a>
                    </div>
                    """
                elif is_video:
                    # Video dosyaları için
                    attachment_html = f"""
                    <div class="chatlog__attachment">
                        <video class="chatlog__attachment-media" controls>
                            <source src="{url}" type="video/{file_ext}">
                            Video görüntülenemiyor
                        </video>
                    </div>
                    """
                elif is_audio:
                    # Ses dosyaları için
                    attachment_html = f"""
                    <div class="chatlog__attachment">
                        <audio controls>
                            <source src="{url}" type="audio/{file_ext}">
                            Ses dosyası oynatılamıyor
                        </audio>
                        <div style="margin-top: 5px;">
                            <a href="{url}" target="_blank" class="chatlog__attachment-download-button">
                                {escape(filename)} ({size_text})
                            </a>
                        </div>
                    </div>
                    """
                else:
                    # Diğer tüm dosya türleri için (belge, PDF, ZIP vb.)
                    attachment_html = f"""
                    <div class="chatlog__attachment">
                        <div class="chatlog__attachment-generic">
                            <svg class="chatlog__attachment-generic-icon" viewBox="0 0 720 960">
                                <use href="#attachment-icon"></use>
                            </svg>
                            <div class="chatlog__attachment-generic-info">
                                <div class="chatlog__attachment-generic-name">{escape(filename)}</div>
                                <div class="chatlog__attachment-generic-size">{size_text}</div>
                                <a href="{url}" target="_blank" class="chatlog__attachment-download-button">
                                    İndir
                                </a>
                            </div>
                        </div>
                    </div>
                    """
                
                attachments_html += attachment_html
            except Exception as e:
                print(f"Ek işlenirken hata: {str(e)}")
        
        return attachments_html

    def format_embeds(self, embeds):
        if not embeds:
            return ""
        
        embeds_html = ""
        
        for i, embed in enumerate(embeds):
            try:
                # Çok basit resim embed'i için kontrol (sadece URL içeren)
                if embed.get('type') == 'image' and not embed.get('title') and not embed.get('description'):
                    image_url = embed.get('url', '')
                    if image_url:
                        embeds_html += f"""
                        <div class="chatlog__embed">
                            <a href="{image_url}" target="_blank">
                                <img class="chatlog__embed-generic-image" src="{image_url}" alt="Embedded image" loading="lazy">
                            </a>
                        </div>
                        """
                        continue
                
                # Twitter, Instagram gibi platformlar için özel kontrol
                is_social_media = False
                if embed.get('provider', {}).get('name') in ['Twitter', 'X', 'Instagram', 'Facebook']:
                    is_social_media = True
                
                # Embed rengi
                embed_color = f"rgba({(embed.get('color') >> 16) & 0xFF},{(embed.get('color') >> 8) & 0xFF},{embed.get('color') & 0xFF},255)" if isinstance(embed.get('color'), int) else "rgba(255,0,0,255)"
                
                # Embed yazar bölümü
                embed_author = ""
                if embed.get('author'):
                    author_name = escape(embed.get('author', {}).get('name', ''))
                    author_url = embed.get('author', {}).get('url', '')
                    author_icon = embed.get('author', {}).get('icon_url', '')
                    
                    author_icon_html = f'<img class="chatlog__embed-author-icon" src="{author_icon}" alt="Author icon">' if author_icon else ''
                    author_link_start = f'<a class="chatlog__embed-author-link" href="{author_url}">' if author_url else ''
                    author_link_end = '</a>' if author_url else ''
                    
                    embed_author = f"""
                    <div class="chatlog__embed-author-container">
                        {author_icon_html}{author_link_start}<div class="chatlog__embed-author">{author_name}</div>{author_link_end}
                    </div>
                    """
                
                # Embed başlık
                embed_title = ""
                if embed.get('title'):
                    title_text = escape(embed.get('title', ''))
                    if embed.get('url'):
                        embed_title = f'<div class="chatlog__embed-title"><a class="chatlog__embed-title-link" href="{embed.get("url")}" target="_blank"><div class="chatlog__markdown chatlog__markdown-preserve">{title_text}</div></a></div>'
                    else:
                        embed_title = f'<div class="chatlog__embed-title">{title_text}</div>'
                
                # YouTube video kontrolü
                embed_youtube = ""
                is_youtube = False
                if embed.get('provider', {}).get('name') == 'YouTube' and embed.get('url'):
                    video_url = embed.get('url')
                    if 'youtube.com/watch?v=' in video_url or 'youtu.be/' in video_url:
                        video_id = ""
                        if 'youtube.com/watch?v=' in video_url:
                            video_id = video_url.split('v=')[1].split('&')[0]
                        elif 'youtu.be/' in video_url:
                            video_id = video_url.split('youtu.be/')[1].split('?')[0]
                        
                        if video_id:
                            embed_youtube = YOUTUBE_EMBED_TEMPLATE.replace("{{video_id}}", video_id)
                            is_youtube = True
                
                # Diğer embed bileşenleri
                embed_description = ""
                if embed.get('description'):
                    description_text = escape(embed.get('description', ''))
                    embed_description = f'<div class="chatlog__embed-description">{description_text}</div>'
                
                embed_fields = ""
                if embed.get('fields'):
                    fields_html = []
                    for field in embed.get('fields', []):
                        field_name = escape(field.get('name', ''))
                        field_value = escape(field.get('value', '')).replace('\n', '<br>')
                        field_inline = 'chatlog__embed-field--inline' if field.get('inline') else ''
                        
                        field_html = f"""
                        <div class="chatlog__embed-field {field_inline}">
                            <div class="chatlog__embed-field-name">{field_name}</div>
                            <div class="chatlog__embed-field-value">{field_value}</div>
                        </div>
                        """
                        fields_html.append(field_html)
                    
                    embed_fields = f'<div class="chatlog__embed-fields">{"".join(fields_html)}</div>'
                
                embed_thumbnail = ""
                if embed.get('thumbnail') and embed['thumbnail'].get('url') and not is_youtube:
                    # YouTube embedleri için thumbnail gösterme
                    thumbnail_url = embed['thumbnail'].get('proxy_url', embed['thumbnail'].get('url', ''))
                    embed_thumbnail = f'<div class="chatlog__embed-thumbnail"><img src="{thumbnail_url}" alt="Embed Thumbnail" loading="lazy"></div>'
                
                # Ana Resmi işle
                embed_image = ""
                if embed.get('image') and embed['image'].get('url'):
                    image_url = embed['image'].get('proxy_url') or embed['image'].get('url', '')
                    if image_url:
                        # Sosyal medya embedleri için özel stil
                        img_class = "chatlog__embed-image" + (" social-media-image" if is_social_media else "")
                        embed_image = f"""
                        <div class="chatlog__embed-images chatlog__embed-images--single">
                            <img class="{img_class}" src="{image_url}" alt="Embedded image" loading="lazy">
                        </div>
                        """
                
                embed_footer = ""
                if embed.get('footer'):
                    footer_text = escape(embed.get('footer', {}).get('text', ''))
                    footer_icon = ""
                    if embed['footer'].get('icon_url'):
                        footer_icon = f'<img class="chatlog__embed-footer-icon" src="{embed["footer"]["icon_url"]}" alt="Footer icon">'
                    embed_footer = f'<div class="chatlog__embed-footer">{footer_icon}<span class="chatlog__embed-footer-text">{footer_text}</span></div>'
                
                # Şablonu uygula
                temp_embed = EMBED_TEMPLATE
                temp_embed = temp_embed.replace("{{embed_color}}", embed_color)
                temp_embed = temp_embed.replace("{{embed_author}}", embed_author)
                temp_embed = temp_embed.replace("{{embed_title}}", embed_title)
                temp_embed = temp_embed.replace("{{embed_description}}", embed_description)
                temp_embed = temp_embed.replace("{{embed_fields}}", embed_fields)
                temp_embed = temp_embed.replace("{{embed_thumbnail}}", embed_thumbnail)
                temp_embed = temp_embed.replace("{{embed_footer}}", embed_footer)
                temp_embed = temp_embed.replace("{{embed_image}}", embed_image)
                temp_embed = temp_embed.replace("{{embed_youtube}}", embed_youtube if is_youtube else "")
                
                embeds_html += temp_embed
                
            except Exception as e:
                print(f"Embed işlenirken hata: {str(e)}")
                import traceback
                print(traceback.format_exc())
        
        return embeds_html

    # Byte formatlamak için yardımcı fonksiyon
    def format_bytes(self, bytes_count):
        if bytes_count < 1024:
            return f"{bytes_count} B"
        elif bytes_count < 1024 * 1024:
            return f"{bytes_count / 1024:.2f} KB"
        else:
            return f"{bytes_count / (1024 * 1024):.2f} MB"

async def main():
    print("Discord Self-Bot Chat Exporter")
    print("==============================")
    print("Not: Self-bot kullanımı Discord'un Hizmet Şartları'na aykırı olabilir.")
    
    # Varsayılan token (isteğe bağlı)
    default_token = ""  # Buraya tokeni ekleyebilirsiniz
    
    # Token al
    if default_token:
        token = default_token
        print("Kayıtlı token kullanılıyor.")
    else:
        token = input("Discord Kullanıcı Tokeninizi giriniz: ")
    
    if not token:
        print("Token gerekli!")
        return
    
    # Token doğru formatta mı kontrol et
    if token.startswith('"') and token.endswith('"'):
        token = token[1:-1]
    
    exporter = DiscordSelfBotExporter(token)
    await exporter.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nKullanıcı tarafından iptal edildi.")
    except Exception as e:
        print(f"\nProgramda bir hata oluştu: {e}")