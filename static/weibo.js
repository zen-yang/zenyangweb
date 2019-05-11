var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weibo_id, callback) {
    var path = `/api/weibo/delete?id=${weibo_id}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(comment_id, callback) {
    var path = `/api/comment/delete?id=${comment_id}`
    ajax('GET', path, '', callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = '/api/comment/update'
    ajax('POST', path, form, callback)
}

var weiboTemplate = function(weibo) {
    var w = `
        <div class="weibo-cell" data-id="${weibo.id}">
            <br>
            <span class="weibo-content">${weibo.content}</span>
            <span>from</span>
            <span class="weibo-user">${weibo.weibo_user}</span>
            <button class="weibo-delete">删除微博</button>
            <button class="weibo-edit">编辑</button>
    `
    return w
}


var commentTemplate = function(comment) {
    var c = `
        <div class="comment-cell" data-id="${comment.id}">
            <span class="comment-user">${comment.comment_user}:</span>
            <span class="comment-content">${comment.content}</span>
            <button class="comment-delete">删除评论</button>
            <button class="comment-edit">编辑</button>
        </div>
    `
    return c
}

var weiboUpdateTemplate = function(content) {
    var t = `
        <div class="weibo-update-form">
            <input class="weibo-update-input" value="${content}">
            <button class="weibo-update">更新</button>
        </div>
    `
    return t
}

var commentUpdateTemplate = function(content) {
    var t = `
        <div class="comment-update-form">
            <input class="comment-update-input" value="${content}">
            <button class="comment-update">更新</button>
        </div>
    `
    return t
}

var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    var s = ''
    var commentadd =`
            <br>
            <input id="id-input-comment">
            <button class="id-comment-add">发表新评论</button>
            <br>
            <br>
        </div>
    `
    var comments = weibo.comments

    if (comments == null) {
        var newweiboCell = weiboCell + commentadd
    } else {
        for (var j = 0; j < comments.length; j++) {
            s = s + commentTemplate(comments[j])
        }
        var newweiboCell = weiboCell + s + commentadd
    }

    // 插入 weibo-list
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', newweiboCell)
}

var insertComment = function(comment, weiboCell) {
    var commentCell = commentTemplate(comment)
    // 插入 comment-list
    var commentList = weiboCell.querySelector('#id-input-comment')
    log('commentList', commentList)
    commentList.insertAdjacentHTML('beforebegin', commentCell)
}

var insertUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    var weiboEdit = weiboCell.querySelector('.weibo-edit')
    weiboEdit.insertAdjacentHTML('afterend', updateForm)
}

var insertCommentUpdateForm = function(content, commentCell) {
    var updateForm = commentUpdateTemplate(content)
    var commentEdit = commentCell.querySelector('.comment-edit')
    commentEdit.insertAdjacentHTML('afterend', updateForm)
}

var loadWeibos = function() {
    apiWeiboAll(function(r) {
        console.log('load all', r)
        var weibos = JSON.parse(r)

        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}

var bindEventWeiboDelete = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
    log(event)

    var self = event.target
    log('被点击的元素', self)
    log('微博删除按钮的classList', self.classList)

    if (self.classList.contains('weibo-delete')) {
        log('点到了删除按钮')
        weiboId = self.parentElement.dataset['id']
        apiWeiboDelete(weiboId, function(response) {
            var r = JSON.parse(response)
            log('apiWeiboDelete', r.message)
            if (r.message == '403'){
                alert('权限不足')
            } else {
                // 删除 self 的父节点
                self.parentElement.remove()
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
    log(event)

    var self = event.target
    log('被点击的元素', self)

    log(self.classList)
    if (self.classList.contains('weibo-edit')) {
        log('点到了编辑按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        var weiboSpan = weiboCell.querySelector('.weibo-content')
        var content = weiboSpan.innerText
        // 插入编辑输入框
        insertUpdateForm(content, weiboCell)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
    log(event)

    var self = event.target
    log('被点击的元素', self)
    log('被点击的元素classList', self.classList)

    if (self.classList.contains('weibo-update')) {
        log('点到了更新按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = weiboCell.dataset['id']
        log('update weibo id', weiboId)
        input = weiboCell.querySelector('.weibo-update-input')
        content = input.value
        log('content内容', content)
        var form = {
            id: weiboId,
            content: content,
        }

        apiWeiboUpdate(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            log('apiWeiboUpdate', weibo)
            if (weibo.message == '403'){
                alert('权限不足')
            }else{
                var weiboSpan = weiboCell.querySelector('.weibo-content')
                weiboSpan.innerText = weibo.content
            }
                var updateForm = weiboCell.querySelector('.weibo-update-form')
                updateForm.remove()
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentAdd = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
    log(event)

    var self = event.target
    log('被点击的元素', self)
    log(self.classList)

    if (self.classList.contains('id-comment-add')) {
        log('点到了评论添加按钮')
        weiboCell = self.closest('.weibo-cell')
        weiboId = self.parentElement.dataset['id']
        var commentInput = weiboCell.querySelector('#id-input-comment')
        var content = commentInput.value
        log('click comment add', content)
        var form = {
            weibo_id:  weiboId,
            content: content,
        }
        log('前端要发送的数据', form)
        apiCommentAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var comment = JSON.parse(r)
            log('要加载的数据', comment)
            insertComment(comment, weiboCell)
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentDelete = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
    log(event)

    var self = event.target
    log('被点击的元素', self)
    log(self.classList)

    if (self.classList.contains('comment-delete')) {
        log('点到了评论删除按钮')
        commentId = self.parentElement.dataset['id']
        apiCommentDelete(commentId, function(response) {
            var r = JSON.parse(response)
            log('apiCommentDelete', r.message)
            if (r.message == '403'){
                alert('权限不足')
            }else{
                // 删除 self 的父节点
                self.parentElement.remove()
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentEdit = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
    log(event)

    var self = event.target
    log('被点击的元素', self)
    log(self.classList)

    if (self.classList.contains('comment-edit')) {
        log('点到了评论编辑按钮')
        commentCell = self.closest('.comment-cell')
        commentId = commentCell.dataset['id']
        log('commentId', commentId)
        var commentSpan = commentCell.querySelector('.comment-content')
        var content = commentSpan.innerText
        log('commentcontent',content)
        // 插入编辑输入框
        insertCommentUpdateForm(content, commentCell)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')

    weiboList.addEventListener('click', function(event) {
    log(event)

    var self = event.target
    log('被点击的元素', self)
    log('被点击的元素classList', self.classList)

    if (self.classList.contains('comment-update')) {
        log('点到了评论更新按钮')
        commentCell = self.closest('.comment-cell')
        commentId =commentCell.dataset['id']
        input = commentCell.querySelector('.comment-update-input')
        content = input.value
        var form = {
            id: commentId,
            content: content,
        }

        apiCommentUpdate(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var comment = JSON.parse(r)
            log('apiCommentUpdate', comment)

            if (comment.message == '403'){
                alert('权限不足')
            } else{
                var commentSpan = commentCell.querySelector('.comment-content')
                commentSpan.innerText = comment.content
            }
                var updateForm = commentCell.querySelector('.comment-update-form')
                updateForm.remove()
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
