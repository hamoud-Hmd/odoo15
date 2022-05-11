odoo.define('freightDashboard.freightDashboard', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var web_client = require('web.web_client');
    var _t = core._t;
    var QWeb = core.qweb;
    var self = this;
    var currency;
    var ActionMenu = AbstractAction.extend({

        contentTemplate: 'familyDashboard',

        renderElement: function (ev) {
            var self = this;
            $.when(this._super())
                .then(function (ev) {

                    //loading Current Budget
                    rpc.query({

                        model: "family.budget",
                        method: 'search_read',
                        args: [[], []],
                    }).then(function (result) {
                        let budget = result[0]

                        // Create our number formatter.
                        let formatter = new Intl.NumberFormat('en-US', {
                            style: 'currency',
                            currency: 'MRO',
                        });


                        $('#current_budget_value').empty().append(formatter.format(budget.active_total));


                        const data = {
                            labels: ['المصروفات', 'المساهمات'],
                            datasets: [
                                {
                                    label: 'Current Budget',
                                    data: [budget.withdraw_total, budget.contribution_total],
                                    backgroundColor: ['#df4759', '#42ba96'],
                                }
                            ]
                        };


                        const config = {
                            type: 'pie',
                            data: data,
                            options: {
                                responsive: true,
                                plugins: {
                                    legend: {
                                        position: 'top',
                                    },
                                    title: {
                                        display: true,
                                        text: 'Chart.js Pie Chart'
                                    }
                                }
                            },
                        };

                        let chartProgressBudget = document.getElementById("current_budget_chart");
                        if (chartProgressBudget) {
                            let myChartCircle = new Chart(chartProgressBudget,
                                config,
                            );
                        }
                    })

                    //loading age range
                    rpc.query({
                        model: "family.member",
                        method: 'search_read',
                        args: [[], []],
                    })
                        .then(function (result) {

                            result = result.filter(r => r.is_active)


                            $('#members_statics_value').empty().append(result.length);

                            const data = {
                                labels: ['الشباب','الرجال', 'المسنين'],
                                datasets: [
                                    {
                                        label: 'Current Budget',
                                        data: [result.filter(m => m.age > 17 && m.age <= 40).length, result.filter(m => m.age > 40 && m.age <= 60).length, result.filter(m => m.age > 60).length],
                                        backgroundColor: [ '#00AAB5', '#e64298','#bb9ba8'],
                                    }
                                ]
                            };


                            const config = {
                                type: 'pie',
                                data: data,
                                options: {
                                    responsive: true,
                                    plugins: {
                                        legend: {
                                            position: 'top',
                                        },
                                        title: {
                                            display: true,
                                            text: 'Chart.js Pie Chart'
                                        }
                                    }
                                },
                            };

                            let chartProgressMembers = document.getElementById("members_statics_chart");
                            if (chartProgressMembers) {
                                let myChartCircle = new Chart(chartProgressMembers,
                                    config,
                                );
                            }
                        })

                    //loading Top 5 members
                    rpc.query({
                        model: "family.member",
                        method: "search_read",
                        args: [[], []]
                    })
                        .then(function (result) {
                            let members = result
                            let formatter = new Intl.NumberFormat('en-US', {
                                style: 'currency',
                                currency: 'MRO',
                            });

                            members.sort((a, b) => (a.total_cost < b.total_cost) ? 1 : ((b.total_cost < a.total_cost) ? -1 : 0))

                            $('#top_5_members_row').empty()
                            members.slice(0, 5).map(c => {
                                $('#top_5_members_row').append(
                                    `
                                        <tr>
                                        <td id="member_${c.id}">${c.name}</td>
                                        <td>${formatter.format(c.total_cost)}</td>
                                        </tr>
                                   `
                                )
                                $("#member_" + c.id).on("click", function (ev) {
                                    self.do_action({
                                        res_model: 'family.member',
                                        name: _t('Member'),
                                        views: [
                                            [false, 'form']
                                        ],
                                        type: 'ir.actions.act_window',
                                        res_id: c.id,
                                    });
                                });
                            })


                        })


                    //loading Debt members
                    rpc.query({
                        model: "family.member",
                        method: "search_read",
                        args: [[], []]
                    }).then(function (result) {
                        // Create our number formatter.
                        let formatter = new Intl.NumberFormat('en-US', {
                            style: 'currency',
                            currency: 'MRO',
                        });
                        let members = result.filter(r => r.debt > 0 && r.is_active)

                        members.sort((a, b) => (a.debt < b.debt) ? 1 : ((b.debt < a.debt) ? -1 : 0))

                        $('#debt_members').empty()
                        members.map(c => {
                            $('#debt_members').append(
                                `
                                        <tr>
                                        <td id="member_${c.id}">${c.name}</td>
                                        <td>${formatter.format(c.debt)}</td>
                                        </tr>
                                   `
                            )
                            $("#member_" + c.id).on("click", function (ev) {
                                self.do_action({
                                    res_model: 'family.member',
                                    name: _t('Member'),
                                    views: [
                                        [false, 'form']
                                    ],
                                    type: 'ir.actions.act_window',
                                    res_id: c.id,
                                });
                            });
                        })


                    })


                    const data = {
                        labels: ['يناير', 'فبراير', 'مارس', 'ابريل', 'مايو', 'يونيو', 'يوليو', 'اغسطس', 'سبتمبر', 'اكتوبر', 'نوفمبر', 'ديسمبر'],
                        datasets: [
                            {
                                label: 'المصروفات',
                                data: [],
                                borderColor: '#df4759',
                                backgroundColor: 'transparent',
                            },
                            {
                                label: 'المساهمات',
                                data: [],
                                borderColor: '#42ba96',
                                backgroundColor: 'transparent',
                            }
                        ]
                    };


                    //loading Contributions
                    rpc.query({
                        model: "family.contribution",
                        method: "search_read",
                        args: [[], []]
                    })
                        .then(function (result) {
                            console.log("contr")
                            let values = []
                            for (let month = 0; month < 12; month++) {
                                const currentDate = new Date().getFullYear() + "-" + (month > 9 ? month + 1 : '0' + (month + 1))
                                let month_vals = result.filter(r => r.create_date.slice(0, 7) === currentDate)
                                let month_total_amount = 0
                                month_vals.map(m => month_total_amount += m.amount)
                                values.push(month_total_amount)
                            }
                            data.datasets[1].data = values
                        });

                    //loading withdraws
                    rpc.query({
                        model: "family.withdraw",
                        method: "search_read",
                        args: [[], []]
                    })
                        .then(function (result) {
                            console.log("withdr")

                            let values1 = []
                            for (let month = 0; month < 12; month++) {
                                const currentDate = new Date().getFullYear() + "-" + (month > 9 ? month + 1 : '0' + (month + 1))
                                // if (month <= (new Date().getMonth())) {
                                let month_vals = result.filter(r => r.create_date.slice(0, 7) === currentDate)
                                let month_total_amount = 0
                                month_vals.map(m => month_total_amount += m.amount)
                                values1.push(month_total_amount)
                                // }
                            }
                            data.datasets[0].data = values1

                            const config = {
                                type: 'line',
                                data: data,
                                options: {
                                    responsive: true,
                                    plugins: {
                                        legend: {
                                            position: 'top',
                                        },
                                        title: {
                                            display: true,
                                            text: 'Chart.js Line Chart'
                                        }
                                    }
                                },
                            };
                            let contributionsWithdrawsChart = document.getElementById("contributionsWithdraws");
                            if (contributionsWithdrawsChart) {
                                let myChartCircle = new Chart(contributionsWithdrawsChart,
                                    config,
                                );
                            }
                        });


                });
        },

    });

    core.action_registry.add('family_dashboard', ActionMenu);

});