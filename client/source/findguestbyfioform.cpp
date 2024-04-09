#include "findguestbyfioform.h"
#include "ui_findguestbyfioform.h"

FindGuestByFioForm::FindGuestByFioForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::FindGuestByFioForm)
{
    ui->setupUi(this);
}

FindGuestByFioForm::~FindGuestByFioForm()
{
    delete ui;
}

void FindGuestByFioForm::clear()
{
    this->ui->fullName->clear();
}

void FindGuestByFioForm::on_FindGuestByFioBtn_clicked()
{
    QString data = "findGuestByFio;" + this->ui->fullName->text();
    emit sendData(data);
}

