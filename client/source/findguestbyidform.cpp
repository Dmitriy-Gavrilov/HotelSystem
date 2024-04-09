#include "findguestbyidform.h"
#include "ui_findguestbyidform.h"

FindGuestByIdForm::FindGuestByIdForm(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::FindGuestByIdForm)
{
    ui->setupUi(this);
}

FindGuestByIdForm::~FindGuestByIdForm()
{
    delete ui;
}

void FindGuestByIdForm::clear()
{
    this->ui->passport->clear();
}

void FindGuestByIdForm::on_findGuestByIdBtn_clicked()
{
    QString data = "findGuestById;" + this->ui->passport->text();
    emit sendData(data);
}

