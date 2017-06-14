$(document).ready(function () {
    function t(t) {
        $("#user-" + t).slideUp("fast")
    }

    function e(t, e) {
        switch (price = "", t = $('[name="account-type"]:checked').val(), e = $('[name="account-duration"]:checked').val(), t) {
            case"pro":
                switch (e) {
                    case"month":
                        price = "1.99";
                        break;
                    case"year":
                        price = "9.99";
                        break;
                    case"lifetime":
                        price = "24.99"
                }
                break;
            case"super-pro":
                switch (e) {
                    case"month":
                        price = "3.99";
                        break;
                    case"year":
                        price = "29.99";
                        break;
                    case"lifetime":
                        price = "74.99"
                }
        }
        $("#plan-price").html("$" + price)
    }

    $('[name="account-type"]').on("change", function () {
        e()
    }), $('[name="account-duration"]').on("change", function () {
        e()
    }), $('[name="account-duration"]') && $('[name="account-type"]') && e(), $(document).on("mouseenter", ".button-removerequest", function () {
        $(this).html("Remove Request")
    }), $(document).on("mouseleave", ".button-removerequest", function () {
        $(this).html("Pending Request")
    }), $(document).on("click", ".button-options", function () {
        var t = $(this).attr("data-id"), e = $(this);
        $("#suboptions-" + t).is(":visible") ? $("#suboptions-" + t).hide() : $("#suboptions-" + t).show()
    }), $(document).on("click", ".button-unfollow", function () {
        var e = $(this).attr("data-id"), a = $(this);
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/unfollow",
            data: {twitUser: e},
            success: function () {
                a.html("Unfollowed"), a.removeClass("button-unfollow").addClass("button-unfollowed"), $("#hide-user").is(":checked") && t(e)
            },
            error: function () {
            }
        }), !1
    }), $(document).on("click", ".button-follow", function () {
        var e = $(this).attr("data-id"), a = $(this).data("screen_name"), i = $(this);
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/follow",
            data: {twitUser: e, screen_name: a},
            success: function (s) {
                i.html("Followed"), $("#hide-user").is(":checked") && t(e), $("#sayhi-user").is(":checked") && $.ajax({
                    type: "POST",
                    url: "/twitter/sayhello",
                    data: {screen_name: a},
                    success: function (t) {
                        i.html("Tweeted")
                    }
                })
            }
        }), !1
    }), $(document).on("click", ".button-block", function () {
        var e = $(this).attr("data-id"), a = $(this);
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/block",
            data: {twitUser: e},
            success: function () {
                a.html("Blocked"), $("#user-" + e + " .user-overlay").show(), $("#user-" + e + " .user-overlay").html("<h6>BLOCKED</h6>"), setTimeout(function () {
                    t(e)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-unblock", function () {
        var e = $(this).attr("data-id"), a = $(this);
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/unblock",
            data: {twitUser: e},
            success: function () {
                a.html("Blocked"), $("#user-" + e + " .user-overlay").show(), $("#user-" + e + " .user-overlay").html("<h6>UNBLOCKED</h6>"), setTimeout(function () {
                    t(e)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-mute", function () {
        var e = $(this).attr("data-id"), a = $(this);
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/mute",
            data: {twitUser: e},
            success: function () {
                a.html("Muted"), $("#user-" + e + " .user-overlay").show(), $("#user-" + e + " .user-overlay").html("<h6>MUTED</h6>"), setTimeout(function () {
                    t(e)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-unmute", function () {
        var e = $(this).attr("data-id"), a = $(this);
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/unmute",
            data: {twitUser: e},
            success: function () {
                a.html("Unmuted"), $("#user-" + e + " .user-overlay").show(), $("#user-" + e + " .user-overlay").html("<h6>UNMUTED</h6>"), setTimeout(function () {
                    t(e)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-removerequest", function () {
        var e = $(this).attr("data-id");
        $(this).attr("disabled", "disabled");
        var a = $(this);
        return $.ajax({
            type: "POST", url: "/twitter/force_unfollow", data: {twitUser: e}, success: function () {
                a.html("Request Removed"), $("#user-" + e + " .user-overlay").show(), $("#user-" + e + " .user-overlay").html("<h6>REMOVED FOLLOW REQUEST</h6>"), setTimeout(function () {
                    t(e)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-forceunfollow", function () {
        var e = $(this).attr("data-id");
        $(this).attr("disabled", "disabled");
        var a = $(this);
        return $.ajax({
            type: "POST", url: "/twitter/force_unfollow", data: {twitUser: e}, success: function () {
                a.html("Force Unfollowed"), $("#user-" + e + " .user-overlay").show(), $("#user-" + e + " .user-overlay").html("<h6>FORCE<br />UNFOLLOWED</h6>"), setTimeout(function () {
                    t(e)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-nofollowlist", function () {
        var e = $(this), a = $(this).attr("data-id");
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/blacklist",
            data: {twitUser: a},
            success: function () {
                e.html("Blacklisted"), $("#user-" + a + " .user-overlay").show(), $("#user-" + a + " .user-overlay").html("<h6>Added To<br />Blacklist</h6>"), setTimeout(function () {
                    t(a)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-nofollowlistremove", function () {
        var e = $(this), a = $(this).attr("data-id");
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/blacklist_remove",
            data: {twitUser: a},
            success: function () {
                e.html("Removed from Blacklist"), $("#user-" + a + " .user-overlay").show(), $("#user-" + a + " .user-overlay").html("<h6>Removed From<br />Blacklist</h6>"), setTimeout(function () {
                    t(a)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-nounfollowlist", function () {
        var e = $(this), a = $(this).attr("data-id");
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/whitelist",
            data: {twitUser: a},
            success: function () {
                e.html("Whitelisted"), $("#user-" + a + " .user-overlay").show(), $("#user-" + a + " .user-overlay").html("<h6>Added To<br />Whitelist</h6>"), setTimeout(function () {
                    t(a)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-nounfollowlistremove", function () {
        var e = $(this), a = $(this).attr("data-id");
        return $(this).attr("disabled", "disabled"), $.ajax({
            type: "POST",
            url: "/twitter/whitelist_remove",
            data: {twitUser: a},
            success: function () {
                e.html("Removed from Whitelist"), $("#user-" + a + " .user-overlay").show(), $("#user-" + a + " .user-overlay").html("<h6>Removed From<br />Whitelist</h6>"), setTimeout(function () {
                    t(a)
                }, 500)
            }
        }), !1
    }), $(document).on("click", ".button-tweet", function () {
        var t = $(this).attr("data-tweet"), e = $(this);
        if ($(this).attr("disabled", "disabled"), $("#tweet-this").val()) {
            var t = $("#tweet-this").val();
            $("#tweet-this").replaceWith("<p>" + t + "</p>"), $.ajax({
                type: "POST",
                url: "/ajax/save_tweet",
                data: {tweet: t},
                success: function () {
                }
            })
        }
        return $.ajax({
            type: "POST", url: "/twitter/tweet", data: {tweet: t}, success: function (t) {
                e.html('<i class="fa fa-check-square-o"></i> Thank You!'), $(".alert.tweet").slideUp("fast")
            }
        }), !1
    }), $(document).on("click", ".button-customize", function () {
        var t = $("#tweet").text();
        $("#tweet").replaceWith('<textarea style="width: 95%; height: 45px; margin: 3px 0 6px; padding: 5px;" id="tweet-this">' + t + '</textarea><div id="charCount" style="text-align: right; margin-right: 5%; font-size: .75em;"></div>')
    }), $(document).on("keyup", "#tweet-this", function () {
        var t = 130, e = $(this).val().length;
        if (e >= t)$("#charCount").text(" you have reached the limit"), $("#tweet-this").val($("#tweet-this").val().substring(0, t)); else {
            var a = t - e;
            $("#charCount").text(a + " characters left")
        }
    }), $(".pagination").on("click", "a", function (t) {
        t.preventDefault();
        var e = $(this).data("total_pages"), a = $(this).data("page"), i = $(this).attr("href"), s = $(this).data("group"), o = $(this).data("order");
        return $(".pagination_" + s + " a").html("Getting Another 100"), $.ajax({
            type: "POST",
            url: i,
            data: {order: o, page: a},
            success: function (t) {
                a += 1, $("#" + s + "_group").append(t), e > a ? ($(".pagination_" + s + " a").html("See Another 100"), $(".pagination_" + s + " a").data("order", o).data("page", a).data("total_pages", e).data("group", s).attr("href", i)) : $(".pagination_" + s).html("That's All Folks")
            }
        }), !1
    }), $("#account-activity").change(function () {
        $("#account-activity").val() > 0 ? (time = $("#account-activity").val() / 1, now = new Date, now = now.getTime() / 1e3, active = now - time, $(".user_miniprofile").each(function () {
            $(this).data("activity") > active && $(this).addClass("hide")
        })) : $(".user_miniprofile").removeClass("hide")
    }), $("#account-age").change(function () {
        $("#account-age").val() > 0 ? (time = $("#account-age").val() / 1, now = new Date, now = now.getTime() / 1e3, active = now - time, $(".user_miniprofile").each(function () {
            $(this).data("accountage") > active ? $(this).addClass("hide") : $(this).removeClass("hide")
        })) : $(".user_miniprofile").removeClass("hide")
    }), $(".order").on("click", "a", function (t) {
        t.preventDefault();
        var e = $(this).data("order"), a = $(this).data("group"), i = $(this).data("url"), s = $(this), o = 0;
        $("#" + a + "_group").html('<h4 class="pure-u-1">Reversing Order...</h4>'), $("#options_" + a + " .option").removeClass("active"), $.ajax({
            type: "POST",
            url: i,
            data: {order: e, page: o},
            success: function (t) {
                $("#" + a + "_group").html(t), s.addClass("active"), $(".pagination_" + a + " a").data("order", e), $(".pagination_" + a + " a").data("page", 1)
            }
        })
    }), $("#wum_email").blur(function () {
        var t = $(this).val();
        return $.ajax({
            type: "POST",
            url: "/main/validate_email",
            data: {email: t},
            dataType: "json",
            success: function (t) {
                t.invalid ? (invalid_fail = 1, $("#wum_email_invalid").html('<i class="fa fa-times"></i> You must enter a valid email address ')) : (invalid_fail = 0, $("#wum_email_invalid").empty()), t.repeat ? (repeat_fail = 1, $("#wum_email_repeat").html('<i class="fa fa-times"></i> That email is already associated with a WUM account')) : (repeat_fail = 0, $("#wum_email_repeat").empty()), invalid_fail || repeat_fail ? $("#submit-checkout").attr("disabled", "disabled") : $("#submit-checkout").removeAttr("disabled")
            }
        }), !1
    }), $(document).on("change", "#history-select", function () {
        monthyear = $(this).val(), $("#history-section").html('<h2 class"loading">Loading New History</h2>'), $.ajax({
            type: "POST",
            url: "/pro/history_select",
            data: {monthyear: monthyear},
            dataType: "html",
            success: function (t) {
                $("#history-section").html(t)
            }
        })
    })
});