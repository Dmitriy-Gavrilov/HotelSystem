#ifndef ADDGUESTFORM_H
#define ADDGUESTFORM_H

#include <QWidget>
#include <QObject>
#include <QIntValidator>

#include "baseform.h"


namespace Ui {
class addGuestForm;
}

class addGuestForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit addGuestForm(QWidget *parent = nullptr);
    ~addGuestForm();
    void clear() override;

signals:
     void sendData(const QString &data);

private slots:
    void on_addGuestBtn_clicked();

private:
    Ui::addGuestForm *ui;
};

#endif // ADDGUESTFORM_H
